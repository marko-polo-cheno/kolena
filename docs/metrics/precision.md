---
search:
  exclude: true
---

# Precision

<div class="grid" markdown>
<div markdown>
Precision measures the proportion of **positive inferences** from a model that are correct, ranging from 0 to 1 (where
1 is best).

As shown in this diagram, precision is the fraction all inferences that are correct:

$$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}$$

In the above formula, $\text{TP}$ is the number of true positive inferences and $\text{FP}$ is the number of false
positive inferences.

!!! info "Guide: True Positive / False Positive"

    Read the [TP / FP / FN / TN](./tp-fp-fn-tn.md) guide if you're not familiar with "TP" and "FP" terminology.

</div>

<figure markdown>
  ![Precision and recall from Wikipedia](../assets/images/metrics-precision-recall.png)
  <figcaption markdown>Placeholder diagram of precision and recall from [Wikipedia](https://en.wikipedia.org/wiki/Precision_and_recall#Precision)
</figure>
</div>

<div class="grid cards" markdown>
- :kolena-manual-16: API Reference: [`precision`][kolena.workflow.metrics.precision] ↗
</div>


## Implementation Details

Precision is used across a wide range of workflows, including classification, object detection, instance segmentation,
semantic segmentation, and information retrieval. It is especially useful when the objective is to measure and reduce
**false positive** inferences.

For most tasks, precision metric is the ratio of the number of correct positive predictions to
the total number of positive predictions:

$$\text{Precision} = \frac{\text{# True Positives}}{\text{# True Positives} + \text{# False Positives}}$$

For workflows with a localization component, such as object detection and instance segmentation, see the
[Geometry Matching](./geometry-matching.md) guide to learn how to compute true positive and false positive counts.

### Examples

Perfect inferences:

<div class="grid" markdown>
| Metric | Value |
| --- | --- |
| TP | 20 |
| FP | 0 |

$$
\begin{align}
\text{Precision} &= \frac{20}{20 + 0} \\[1em]
&= 1.0
\end{align}
$$
</div>

Partially correct inferences:

<div class="grid" markdown>
| Metric | Value |
| --- | --- |
| TP | 90 |
| FP | 10 |

$$
\begin{align}
\text{Precision} &= \frac{90}{90 + 10} \\[1em]
&= 0.9
\end{align}
$$
</div>

Zero positive inferences:

<div class="grid" markdown>
| Metric | Value |
| --- | --- |
| TP | 0 |
| FP | 20 |

$$
\begin{align}
\text{Precision} &= \frac{0}{0 + 20} \\[1em]
&= 0.0
\end{align}
$$
</div>

### Multiple Classes

So far, we have only looked at **binary** classification/object detection cases, but in **multi-class** or
**multi-label** cases, precision is computed per class. In the [TP / FP / FN / TN](./tp-fp-fn-tn.md) guide,
we went over multiple-class cases and how these metrics are computed. Once you have these four metrics computed per
class, you can compute precision for each class by treating each as a single-class problem.

### Aggregating Per-class Metrics

If you are looking for a **single** precision score that summarizes model performance across all classes, there are
different ways to aggregate per-class precision scores: **macro**, **micro**, and **weighted**. Read more about these
methods in the [Averaging Methods](./averaging-methods.md) guide.

## Limitations and Biases

As seen in its formula, precision only takes **positive** inferences (TP and FP) into account; negative inferences
(TN and FN) are not considered. Thus, precision only provides one half of the picture, and should always be used in
tandem with recall: recall penalizes false negatives, whereas precision does not.

For a single metric that takes both precision and recall into account, use F1 score, which is the harmonic mean between
precision and recall.