# Figure, table, and quantitative consistency review

Review each object at three distinct layers. Passing one layer does not establish the others.

## Contents

- Three-layer audit
- Plan the question and representation
- Scientific and visual checks
- Table semantics and number tracing
- Export, revision, and reporting

## Three-layer audit

| Layer | Evidence required | What it can establish |
|---|---|---|
| Scientific meaning | Manuscript context, caption, metric/design definitions | Whether the object addresses its claim and permits the intended comparison |
| Rendered communication | Actual displayed image or compiled page | Legibility, labeling, layout, visual encoding, clipping, and accessibility |
| Numerical provenance | Source data, transformation code, configuration, logs as available | Whether reported values match the specified computation and source |

List all figures, panels, tables, supplementary objects, and references to them.
For each object record which layers were completed, the viewed version/page, and any missing sources.
Text extraction, filename checks, image dimensions, or a plotting script alone are not visual inspection.
View the actual final rendered object, preferably within the compiled page at intended reading size.
If the host cannot render or view it, report visual inspection as unverified and continue scientific/textual checks.
Pixels alone cannot establish source-data authenticity, independent replication, or exact numerical agreement.
A visually plausible figure is not evidence that the underlying experiment occurred.

## Plan the question and representation

For a new object or major redesign, connect its presentation to the argument before choosing its appearance.

| Field | What to specify |
|---|---|
| Question | The comparison, uncertainty, process, or relationship the reader needs to understand |
| Representation | The form that makes that question inspectable with the available evidence |
| Readout | The exact cell, interval, curve region, panel, or structural feature to examine |
| Consequence | The conclusion, boundary, unresolved alternative, or next decision justified by that observation |

Use a table when exact values matter, a plot for a distribution or trend, and a diagram for structure or flow; use an equation or algorithm when the object to explain is a formal relation or procedure.
Choose according to the reader's task rather than a preferred chart style, and align the sequence with the claim structure in [argument-novelty.md](argument-novelty.md).
An object can establish a null result, assumption, failure regime, or limitation; its consequence need not be a performance gain.
Do not let a visual pattern imply a mechanism or causal explanation that the design cannot identify.
Use as many objects as the argument needs, without a fixed quota of main or supporting figures.
Consolidate redundant displays only when the result preserves necessary detail, uncertainty, and material counterevidence.

## Scientific and visual checks

Start with the claim the object is intended to support.
Ask whether the selected design makes that claim inspectable: comparisons, uncertainty, distribution, mechanism, pipeline, or qualitative example.
Check whether the main text, caption, legend, plotted marks, and supplementary definitions agree.
Require self-contained definitions sufficient for interpretation, with reasonable cross-references for lengthy protocols.
Assess:

- Axes, units, direction, ranges, transforms, normalization, and truncation.
- Color/shape/line encodings and whether they remain distinguishable at publication size.
- Legend labels and ordering, consistent series identity across panels, and explained abbreviations.
- Sample/replicate counts, aggregation, error-bar definition, and the unit on which uncertainty is computed.
- Reference lines, chance levels, baselines, and operating points needed for the intended comparison.
- Bin widths, smoothing, interpolation, clipping, missing values, excluded points, and censored/time-limited runs.
- Representative-example selection and whether failures or counterexamples were suppressed.
- Panel alignment, shared scales, comparable aspect ratios, and labels that survive grayscale or color-vision differences.
- Fonts, contrast, collision, cropped symbols, misplaced annotations, and excessive detail.

An axis need not start at zero in every chart; evaluate whether the scale is explicit and whether the visual impression exaggerates the relevant difference.
Bars encoding magnitude usually require special care with a truncated baseline; time series and distributions may justify a focused range.
Three-dimensional decoration, dual axes, or area encodings are concerns when they distort or obscure the comparison, not automatic scientific errors.
Raster photographs, microscopy images, screenshots, and heatmaps can be appropriate.
Vector export is often useful for line art and text, but the file extension alone does not determine quality or severity.
An em dash in a caption is not a validity issue.
Check whether an architecture diagram distinguishes implemented components, optional branches, training-only paths, and inferred conceptual relationships.
Do not let illustrative arrows imply causality or measured information flow that the study does not establish.
For qualitative generated examples, require the prompt/input, selection rule, relevant settings, and labels distinguishing examples from aggregate evidence.

## Table semantics and number tracing

Check row/column groupings, metric direction, dataset identity, model versions, budgets, units, and footnotes.
Verify that highlighted best values are best under the stated criterion, including ties and uncertainty.
Do not imply significance merely through boldface, rank, or overlapping/nonoverlapping error bars.
Compare precision with measurement and uncertainty; avoid distracting false precision while retaining sufficient information.
Check that totals, percentages, sample counts, confidence intervals, and weighted aggregates use compatible denominators.
Different sample sizes, missing conditions, or exclusions must be visible where they affect the comparison.
Keep a number-trace record:

| Reported object | Source | Transformation | Expected precision | Comparison result |
|---|---|---|---|---|
| Table 2, success, model A | results.csv; declared task/run subset | Equal-task mean of run means | 3 decimals, half-even if specified | Match, mismatch, or unverified |

Specify filtering, grouping, weighting, unit conversion, rounding, and missing-value policy before recomputation.
Do not choose the aggregation that makes the published number fit.
If the paper's intended aggregation is ambiguous, show the plausible results and request clarification.
Compare raw values to the report using its declared rounding/precision policy.
For example, 0.9477 legitimately displays as 0.948 at three decimal places under ordinary nearest rounding.
The difference is not numerical drift; check a published 0.949 or an inconsistent transformation instead.
At exact halfway boundaries, use the declared tie-breaking rule; do not silently mix half-even and half-up.
For displayed percentages, perform the fraction-to-percent conversion before applying display precision.
The values 0.9477, 94.77%, and 94.8% may represent the same quantity at different precision.
An absolute increase from 92% to 94% is 2 percentage points; the relative increase is approximately 2.17%.
Use explicit absolute/relative tolerance only when justified by measurement, computation, or reporting policy.
Do not use a large arbitrary tolerance to conceal a wrong metric, denominator, or configuration.
Reject nonfinite values and hidden empty groups from summaries; label missing observations and the analysis policy.
Check whether a “mean” is actually a best seed, a pooled score, or a row copied from a different model/configuration.
Trace any discrepancy through source version, transformation, and manual copy before attributing a cause.
An inconsistency is evidence for an inconsistency, not evidence of deliberate manipulation.

## Export, revision, and reporting

Inspect the final compiled artifact after any layout or image change.
For raster output, assess effective resolution at the final physical size, not only the metadata DPI field.
For fonts and line widths, use actual page rendering; a large standalone image can hide illegibility after reduction.
Check crop boundaries, transparency, color-space assumptions, embedded fonts where relevant, and journal constraints if verified.
Use plotting or vector tools for precise scientific charts and diagrams tied to exact labels or numbers.
Do not use generative imagery to reconstruct data plots, error bars, axes, numerical tables, or evidence-bearing scientific images.
For an illustrative conceptual image, clearly label its illustrative role and keep it separate from measured evidence.

When authorized to revise, preserve data semantics and record changes to scales, aggregation, exclusions, or selection.
Do not silently redraw a graph with new values or cosmetically remove inconvenient points.
Provide a caption repair when the problem is missing definitions; propose a different chart only when it improves the relevant comparison.
Provide source/data repair when the problem is computation; improved styling cannot resolve a wrong result.
For every object, report: supporting claim, layers inspected, located issues, exact fixes, verification condition, and source gaps.
Severity should follow the effect on interpretation: unreadable decisive results can be major; a harmless local alignment error is usually editorial.
Close a figure finding only after checking the revised rendered object and, when relevant, recomputed source values.
