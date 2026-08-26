# NOTES.md — Week 4: Versioning, Feature Store & Lineage

**Student ID used with `generate_for_student.py`:**
142301040


## v1 vs. v2 manifest comparison

When looking at the manifests in `.feature_store/feature_groups/card_activity/`:
- `feature_group_version_id`: v1 is `"v1"` and v2 is `"v2"`.
- `source_raw_version_id`: v1 links to raw version `"v1"`, and v2 links to raw version `"v2"`.
- `row_count`: v1 has 377 rows (from 500 raw transactions) and v2 has 119 rows (from 125 raw transactions).
- The `schema` and `transform_version` are identical (`["avg_amount", "card_id", "event_time", "max_amount", "pct_card_present", "txn_count"]` and `"v1"`), keeping the feature format consistent across versions even though the raw schema changed.


## Why treat amount_minor_units differently from amount?

In v1, `amount` is in dollars (e.g. 100.0), while in v2 `amount_minor_units` is in cents (e.g. 10000).

If we didn't divide `amount_minor_units` by 100 before computing `avg_amount` and `max_amount`, the v2 feature values would be 100 times larger than the v1 values. Dividing by 100 converts them back to dollars so the aggregates stay in the same unit and can be compared properly across versions.
