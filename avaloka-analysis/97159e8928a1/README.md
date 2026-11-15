# Avaloka mission `99ba26e5c9a4`

**Goal:** how does recharge_delta vary by district

This bundle was produced by Avaloka as a governed *Data Mission* — an outcome, not an interaction. Economic multiplier: **11.1x** (≈11.6 manual hours compressed).

## Deliverables

- `executive_report.html` — the decision-maker summary
- `technical_report.html` — full methodology, schema, quality and validation
- `analysis.ipynb` / `analysis.py` — reproducible pipeline
- `transformed_dataset.parquet` — cleaned working dataset
- `data_quality.json`, `validation_report.json`, `planner_graph.json` — evidence
- `assumptions.yaml`, `lineage.json`, `environment.lock` — governance & reproducibility
- `goal_analysis.json` — measured answer to the stated goal

## Key findings

- district=Rajkot: mean recharge_delta=8.25.
- district=Junagadh: mean recharge_delta=7.44.
- district=Aravalli: mean recharge_delta=6.51.
- district=Porbandar: mean recharge_delta=5.93.
- district=Amreli: mean recharge_delta=5.81.

## Limitations

- High-missingness columns require an explicit imputation policy.
- Estimated manual effort and value are heuristics pending customer calibration.

## Reproduce

```bash
avaloka analyze 'data\processed\gujarat_groundwater_seasonal_paired.csv' --goal 'how does recharge_delta vary by district' --output ./reproduced-analysis
```

---
_Reproduce or adapt this mission with `avaloka`._