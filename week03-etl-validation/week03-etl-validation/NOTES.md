# NOTES.md — Week 3: ETL and Data Validation

**Student ID used with `generate_for_student.py`:**
142301040


## Quarantine count vs. the 7 known injected problems

- Total rows: 600
- Clean rows: 594
- Quarantined rows: 6
- Total violations found: 8

### Why 6 rows quarantined:
- 2 rows (251 and 344) have empty amounts. Each fails both the not-null check and the positive amount check (4 violations on 2 rows).
- 1 row (282) has a negative amount.
- 1 row (164) has a wrong category (`crypto_kiosk`).
- 1 row (551) has a missing card id.
- 1 row (420) is a duplicate transaction id.
- The country code problem is not checked by our suite.

Since rows with multiple errors are only quarantined once, exactly **6 unique rows** are quarantined.
