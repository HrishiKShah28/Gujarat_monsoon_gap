# Avaloka mission `d792d994feea`

**Goal:** Predict 'depth_may_next'

This bundle was produced by Avaloka as a governed *Data Mission* — an outcome, not an interaction. Economic multiplier: **11.1x** (≈20.7 manual hours compressed).

## Deliverables

- `executive_report.html` — the decision-maker summary
- `technical_report.html` — full methodology, schema, quality and validation
- `analysis.ipynb` / `analysis.py` — reproducible pipeline
- `transformed_dataset.parquet` — cleaned working dataset
- `data_quality.json`, `validation_report.json`, `planner_graph.json` — evidence
- `assumptions.yaml`, `lineage.json`, `environment.lock` — governance & reproducibility
- `model/` + `model_card.md` — the validated model and its card
- `evaluation_report.html`, `cost_quality.json` — candidate comparison & economics
- `service.py`, `Dockerfile`, `deployment/` — the deployment package
- `feature_contract.yaml`, `inference_schema.json`, `monitoring_config.yaml` — the serving contract

## Key findings

- 'depth_may' and 'baseline_persistence_pred' are strongly associated (|corr|=1.0).
- 'depth_may' and 'depth_jan_next' are strongly associated (|corr|=0.9817).
- 96.6% missing.
- 96.6% missing.
- Best model 'random_forest' scored 0.9665 r2 on holdout.
- 'depth_may' and 'baseline_persistence_pred' move together (|corr|=1.0); consider redundancy or a shared driver.

## Limitations

- High-missingness columns require an explicit imputation policy.
- Estimated manual effort and value are heuristics pending customer calibration.

## Reproduce

```bash
python analysis.py  # reproduce data preparation
```

## Serve locally

```bash
pip install -r requirements.lock
uvicorn service:app --port 8080
# then: avaloka deploy . --target local
```

---
_Reproduce or adapt this mission with `avaloka`._