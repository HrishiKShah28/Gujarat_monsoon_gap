# Avaloka mission `7063f3ebf45c`

**Goal:** how does depth vary by hydro_zone

This bundle was produced by Avaloka as a governed *Data Mission* — an outcome, not an interaction. Economic multiplier: **11.1x** (≈14.2 manual hours compressed).

## Deliverables

- `executive_report.html` — the decision-maker summary
- `technical_report.html` — full methodology, schema, quality and validation
- `analysis.ipynb` / `analysis.py` — reproducible pipeline
- `transformed_dataset.parquet` — cleaned working dataset
- `data_quality.json`, `validation_report.json`, `planner_graph.json` — evidence
- `assumptions.yaml`, `lineage.json`, `environment.lock` — governance & reproducibility
- `goal_analysis.json` — measured answer to the stated goal

## Key findings

- hydro_zone=North Gujarat Alluvium: mean depth=15.6.
- hydro_zone=Saurashtra Hard-Rock Basalt: mean depth=10.
- hydro_zone=Kachchh Arid Sedimentary: mean depth=9.98.
- hydro_zone=South & Central Gujarat Plain: mean depth=7.49.

## Limitations

- Estimated manual effort and value are heuristics pending customer calibration.

## Reproduce

```bash
avaloka analyze 'data\processed\gujarat_groundwater_analytical.csv' --goal 'how does depth vary by hydro_zone' --output ./reproduced-analysis
```

---
_Reproduce or adapt this mission with `avaloka`._