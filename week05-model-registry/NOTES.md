# NOTES.md — Week 5: Model Registry Governance

**Student ID used with `generate_for_student.py`:**
142301040


## Which candidate reached Production, and why?

candidate_b (registered as v2) reached Production, while candidate_a (v1) was blocked.

candidate_a was blocked at two points:
1. First, promoting v1 without a model card failed with GovernanceError because Production promotion strictly requires a model_card.json.
2. After generating the card, promoting v1 failed again because its F1 score was 0.496, which is below the 0.70 production threshold.

candidate_b succeeded because it had a valid model card and its F1 score was 0.877 (clearing the 0.70 threshold).


## Gating stale feature data

To block models trained on stale feature data (>30 days old):
1. In register_model, we should record the feature timestamp or feature group version creation time in the model's manifest.json (or model card).
2. In promote_model, when target_stage is "Production", we check the training data age by comparing the feature timestamp with the current time. If it's older than 30 days, we raise a GovernanceError blocking promotion.


## Scaling the gate to 40 candidates

What wouldn't change:
- register_model would still assign version numbers (v1 to v40) and store each model/manifest without overwriting previous versions.
- promote_model would still enforce the same governance gate (model card + F1 >= 0.70) and ensure only one version stays in Production by auto-archiving the previous one.
- get_production_model would still scan manifests to find the current Production model.

What would change:
- In practice, we shouldn't register all 40 AutoML runs directly into the production registry. Instead, we would log them to an experiment tracker (like MLflow) and only register the best candidate(s).
- We would need an automated evaluation step to rank the 40 candidates by metric and pick the top one to promote.
- Generating model cards manually for 40 models isn't feasible, so card generation would need to automatically pull metrics and parameters from the run, requiring human review only for the selected production candidate.
