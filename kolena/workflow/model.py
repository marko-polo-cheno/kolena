# Copyright 2021-2023 Kolena Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import dataclasses
import json
from abc import ABCMeta
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypeVar

from pydantic import validate_arguments

from kolena._api.v1.core import Model as CoreAPI
from kolena._api.v1.generic import Model as API
from kolena._utils import krequests
from kolena._utils import log
from kolena._utils.batched_load import _BatchedLoader
from kolena._utils.consts import BatchSize
from kolena._utils.endpoints import get_model_url
from kolena._utils.frozen import Frozen
from kolena._utils.instrumentation import telemetry
from kolena._utils.instrumentation import WithTelemetry
from kolena._utils.serde import from_dict
from kolena._utils.validators import ValidatorConfig
from kolena.errors import NotFoundError
from kolena.workflow import GroundTruth
from kolena.workflow import Inference
from kolena.workflow import TestCase
from kolena.workflow import TestSample as BaseTestSample
from kolena.workflow._datatypes import TestSampleDataFrame
from kolena.workflow._validators import assert_workflows_match
from kolena.workflow.workflow import Workflow


TestSample = TypeVar("TestSample", bound=BaseTestSample)


class Model(Frozen, WithTelemetry, metaclass=ABCMeta):
    """The descriptor of a model tested on Kolena."""

    #: The :class:`kolena.workflow.Workflow` of this model.
    workflow: Workflow

    _id: int

    #: Unique name of the model.
    name: str

    #: Unstructured metadata associated with the model.
    metadata: Dict[str, Any]

    #: Function transforming a :class:`kolena.workflow.TestSample` for a workflow into an
    #: :class:`kolena.workflow.Inference` object. Required when using :meth:`kolena.workflow.test` or
    #: :meth:`kolena.workflow.TestRun.run`.
    infer: Optional[Callable[[TestSample], Inference]]

    @telemetry
    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "workflow"):
            raise NotImplementedError(f"{cls.__name__} must implement class attribute 'workflow'")
        super().__init_subclass__()

    @validate_arguments(config=ValidatorConfig)
    def __init__(
        self,
        name: str,
        infer: Optional[Callable[[TestSample], Inference]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        if type(self) == Model:
            raise Exception("<Model> must be subclassed.")
        try:
            loaded = self.load(name, infer)
            if len(loaded.metadata.keys()) > 0 and loaded.metadata != metadata:
                log.warn(f"mismatch in model metadata, using loaded metadata (loaded: {loaded.metadata})")
        except NotFoundError:
            loaded = self.create(name, infer, metadata)

        self._id = loaded._id
        self.name = loaded.name
        self.metadata = loaded.metadata
        self.infer = infer
        self._freeze()

    @classmethod
    def create(
        cls,
        name: str,
        infer: Optional[Callable[[TestSample], Inference]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "Model":
        """
        Create a new model.

        :param name: the unique name of the new model to create.
        :param infer: optional inference function for this model.
        :param metadata: optional unstructured metadata to store with this model.
        :return: the newly created model.
        """
        metadata = metadata or {}
        request = CoreAPI.CreateRequest(name=name, metadata=metadata, workflow=cls.workflow.name)
        res = krequests.post(endpoint_path=API.Path.CREATE.value, data=json.dumps(dataclasses.asdict(request)))
        krequests.raise_for_status(res)
        obj = cls._from_data_with_infer(from_dict(data_class=CoreAPI.EntityData, data=res.json()), infer)
        log.info(f"created model '{name}' ({get_model_url(obj._id)})")
        return obj

    @classmethod
    def load(cls, name: str, infer: Optional[Callable[[TestSample], Inference]] = None) -> "Model":
        """
        Load an existing model.

        :param name: the name of the model to load.
        :param infer: optional inference function for this model.
        """
        request = CoreAPI.LoadByNameRequest(name=name)
        res = krequests.put(endpoint_path=API.Path.LOAD.value, data=json.dumps(dataclasses.asdict(request)))
        krequests.raise_for_status(res)
        obj = cls._from_data_with_infer(from_dict(data_class=CoreAPI.EntityData, data=res.json()), infer)
        log.info(f"loaded model '{name}' ({get_model_url(obj._id)})")
        return obj

    @validate_arguments(config=ValidatorConfig)
    def load_inferences(self, test_case: TestCase) -> List[Tuple[TestSample, GroundTruth, Inference]]:
        """
        Load all inferences stored for this model on the provided test case.

        :param test_case: the test case for which to load inferences.
        :return: the ground truths and inferences for all test samples in the test case.
        """
        return list(self.iter_inferences(test_case))

    @validate_arguments(config=ValidatorConfig)
    def iter_inferences(self, test_case: TestCase) -> Iterator[Tuple[TestSample, GroundTruth, Inference]]:
        """
        Iterate over all inferences stored for this model on the provided test case.

        :param test_case: the test case over which to iterate inferences.
        :return: an iterator exposing the ground truths and inferences for all test samples in the test case.
        """
        log.info(f"loading inferences from model '{self.name}' on test case '{test_case.name}'")
        assert_workflows_match(self.workflow.name, test_case.workflow.name)
        for df_batch in _BatchedLoader.iter_data(
            init_request=API.LoadInferencesRequest(
                model_id=self._id,
                test_case_id=test_case._id,
                batch_size=BatchSize.LOAD_SAMPLES.value,
            ),
            endpoint_path=API.Path.LOAD_INFERENCES.value,
            df_class=TestSampleDataFrame,
        ):
            for record in df_batch.itertuples():
                test_sample = self.workflow.test_sample_type._from_dict(record.test_sample)
                ground_truth = self.workflow.ground_truth_type._from_dict(record.ground_truth)
                inference = self.workflow.inference_type._from_dict(record.inference)
                yield test_sample, ground_truth, inference
        log.success(f"loaded inferences from model '{self.name}' on test case '{test_case.name}'")

    @classmethod
    def _from_data_with_infer(
        cls,
        data: CoreAPI.EntityData,
        infer: Optional[Callable[[TestSample], Inference]] = None,
    ) -> "Model":
        assert_workflows_match(cls.workflow.name, data.workflow)
        obj = cls.__new__(cls)
        obj._id = data.id
        obj.name = data.name
        obj.metadata = data.metadata
        obj.infer = infer
        obj._freeze()
        return obj
