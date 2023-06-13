---
icon: kolena/cube-16
hide:
  - toc
---

# :kolena-cube-20: `kolena.workflow`

`kolena.workflow` contains the definitions to build a [workflow](../../core-concepts/workflow.md):

!!! info inline end "Defining a workflow"

    [`TestSample`][kolena.workflow.TestSample], [`GroundTruth`][kolena.workflow.GroundTruth], and
    [`Inference`][kolena.workflow.Inference] can be thought of as the data model, or schema, for a workflow.

    See the [workflow](../../core-concepts/workflow.md) developer guide for more information.

1. Design data types, including any [`annotations`](annotation.md) or [`assets`](asset.md):

    - [`TestSample`][kolena.workflow.TestSample]: model inputs, e.g. images, videos, documents
    - [`GroundTruth`][kolena.workflow.GroundTruth]: expected model outputs
    - [`Inference`][kolena.workflow.Inference]: real model outputs

2. Define metrics and how they are computed:

    - [`Evaluator`][kolena.workflow.Evaluator]: metrics computation engine

!!! info inline end "Managing Tests"

    See the [test case and test suite](../../core-concepts/test-suite.md) developer guide for an introduction to the
    test case and test suite concept.

3. Create tests:

    - [`TestCase`][kolena.workflow.TestCase]: a test dataset, or a slice thereof
    - [`TestSuite`][kolena.workflow.TestSuite]: a collection of test cases

4. Test models:

    - [`Model`][kolena.workflow.Model]: descriptor for a model
    - [`test`][kolena.workflow.test]: interface to run tests