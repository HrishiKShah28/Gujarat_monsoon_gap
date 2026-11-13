# Model card — Predict 'depth_may_next'

- **Mission:** `d792d994feea`
- **Task:** regression
- **Target:** depth_may_next
- **Primary metric:** r2
- **Selected model:** random_forest
- **Validation verdict:** PASS (max safe deployment level 4/4)

## Intended use

Decision support for the stated goal. Not a substitute for human judgement on high-stakes decisions.

## Performance

| Candidate | r2 | CV mean ± std |
|---|---|---|
| random_forest | 0.9665 | 0.963 ± 0.006 |
| gradient_boosting | 0.9477 | 0.944 ± 0.006 |
| linear_regression | 0.9109 | 0.887 ± 0.041 |

## Training data

- Rows: 17268 train / 4318 test
- Features: 18

## Limitations & ethical considerations

- High-missingness columns require an explicit imputation policy.
- Estimated manual effort and value are heuristics pending customer calibration.

## Validation checks

- **data_sufficiency** — PASS: ~50 rows/feature suggests >= 900 rows for 18 features.
- **target_leakage** — PASS: No feature is near-perfectly predictive of the target.
- **split_validity** — PASS: Used 'random_train_test' (17268 train / 4318 test rows).
- **beats_baseline** — PASS: CV r2 0.963 beats the mean baseline (-0.000) by more than fold noise.
- **stability** — PASS: CV r2 = 0.963 +/- 0.006 (stable).
- **overfitting** — PASS: Holdout and CV scores are consistent.
