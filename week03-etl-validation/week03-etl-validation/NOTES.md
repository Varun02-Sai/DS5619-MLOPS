# NOTES.md — Week 3: ETL and Data Validation

**Student ID used with `generate_for_student.py`:**
142301040


## Quarantine count vs. the 7 known injected problems

- Total rows: 600
- Clean rows: 594
- Quarantined rows: 6
- Total violations detected: 8

The suite quarantined 6 unique rows. Although 7 problems are injected, the two rows with null amounts trigger both `expect_column_not_null` and `expect_column_positive`. Because rows violating multiple expectations are quarantined only once, 6 distinct rows are quarantined.
