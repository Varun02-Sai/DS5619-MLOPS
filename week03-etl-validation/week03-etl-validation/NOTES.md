# NOTES.md — Week 3: ETL and Data Validation

**Student ID used with `generate_for_student.py`:**
142301040


## Quarantine count vs. the 7 known injected problems

A total of 6 rows were quarantined out of 600 (594 clean rows).

This does not match the 7 known injected problems because:
1. Two rows (indices 251 and 344) have null amounts. They fail both `expect_column_not_null` and `expect_column_positive` because null cannot be converted to a positive float. Since a row with multiple errors is only quarantined once, this produced 4 violations across 2 rows.
2. For the duplicate transaction ID, only the second row (index 420) is flagged as a violation by `expect_column_unique`, while the first occurrence is kept.
3. The invalid country code ('ZZ') is not part of the expectation suite in `build_expectation_suite()`, so it is not checked.

Along with row 282 (negative amount), row 164 (invalid category `crypto_kiosk`), and row 551 (null card_id), this gives 6 quarantined rows in total.
