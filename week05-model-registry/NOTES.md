# NOTES.md — Week 5: Model Registry Governance

**Student ID used with `generate_for_student.py`:**
142301040


## Which candidate reached Production, and why?

`candidate_b` (registered as version `v2`) successfully reached Production, while `candidate_a` (version `v1`) was blocked from promotion.

- **`candidate_a` (v1)**:
  - When promotion was initially attempted without generating a model card, it was blocked by the governance rule enforcing that all Production models must have an accompanying `model_card.json`.
  - After a model card was generated, promotion was attempted again and blocked a second time because its evaluation F1 score was `0.496` (precision: 0.447, recall: 0.556, AUC: 0.529), failing the mandatory quality bar of `PRODUCTION_F1_THRESHOLD = 0.70`.
- **`candidate_b` (v2)**:
  - Once a complete `model_card.json` was generated and validated, `candidate_b` was promoted because its F1 score was `0.877` (precision: 0.920, recall: 0.837, AUC: 0.978), which safely cleared the 0.70 quality threshold.


## Gating stale feature data

To enforce a freshness gate in `promote_model` that blocks models trained on stale feature data (>30 days old):

1. **Lineage / Metadata Tracking**: When registering a model, the manifest must record the lineage timestamp of the upstream training data (e.g. `manifest["lineage"]["feature_timestamp"]` or `manifest["training_data_cutoff_time"]` from the feature store / feature group version metadata created in Week 4).
2. **Freshness Validation Gate**: Inside `promote_model`, when `target_stage == "Production"`:
   - Extract the feature timestamp from `manifest.json`.
   - Compute the elapsed age: `age_days = (datetime.now(timezone.utc) - feature_timestamp).days`.
   - If `age_days > 30`, raise `GovernanceError(f"Cannot promote {name} {version_id} to Production: training feature data is stale ({age_days} days old > 30-day limit)")`.
3. **Audit Trail**: Record the evaluated feature timestamp and freshness check result inside the promotion history entry (`manifest["history"]`) to provide a complete audit trail for compliance.


## Scaling the gate to 40 candidates

Tying back to AutoML/HPO workflows where 40 candidates are produced:

- **What would NOT change**:
  - **Sequential, Immutable Versioning**: `register_model` continues to assign sequential version numbers (`v1` to `v40`) and saves isolated artifacts and manifests for each candidate without overwriting prior runs.
  - **Governance Invariants**: The promotion gate rule in `promote_model` (`f1 >= 0.70` + valid model card) remains intact and strictly gates any candidate entering Production regardless of search scale.
  - **Single Production Invariant**: Promoting any winning version to `Production` automatically transitions whichever version is currently in `Production` to `Archived`.
  - **Registry Queries**: `get_production_model` scans version manifests to identify the single active production model without architectural changes.

- **What WOULD change or need enhancement**:
  - **Experiment Tracking vs. Registry Separation**: In a 40-candidate HPO run, writing all 40 unvalidated trials directly into the top-level model registry pollutes production version history. A best-practice architecture logs all 40 trials to an experiment tracker (e.g., MLflow/W&B runs) and only registers top-k candidate models into the formal model registry.
  - **Automated Leaderboard & Evaluation Gate**: Instead of manually triggering promotion attempts per candidate, an automated evaluation pipeline filters and ranks candidates by metric (e.g. `f1`, `auc`, latency) and selects the best candidate clearing the quality threshold.
  - **Automated Model Card Metadata**: Manually populating 40 distinct model cards is error-prone and tedious. Hyperparameters, dataset version hashes, and metrics should be automatically extracted and populated into `model_card.json`, leaving only qualitative/ethical sections for governance review and human sign-off on the candidate selected for staging/production.
