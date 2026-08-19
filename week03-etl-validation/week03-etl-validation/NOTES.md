# NOTES.md — Week 3: ETL and Data Validation

**Student ID used with `generate_for_student.py`:**
142301040

**Random Seed Generated:**
92466463


## Quarantine count vs. the 7 known injected problems

### Summary of Results:
- Total rows: 600
- Clean rows: 594
- Quarantined rows: 6
- Total violations detected: 8

### Detailed Breakdown of Violations:
1. `expect_column_not_null` (amount): 2 violations (rows 251, 344)
2. `expect_column_not_null` (card_id): 1 violation (row 551)
3. `expect_column_positive` (amount): 3 violations (rows 251, 282, 344)
4. `expect_column_in_set` (merchant_category): 1 violation (row 164)
5. `expect_column_unique` (transaction_id): 1 violation (row 420)

### Explanation of Discrepancy:
1. **Multiple violations on the same row**: 
   - Rows 251 and 344 both have null values in `amount`. This causes each of them to fail two checks at once (`expect_column_not_null` and `expect_column_positive`), counting as 4 violations across only 2 physical rows.
2. **Duplicate transaction ID**:
   - Row 420 duplicates an earlier transaction ID. The first original row is kept, while only the duplicate row is marked as a violation and quarantined.
3. **Unchecked injected problem**:
   - The generator also creates an invalid country code (`ZZ`), but our expectation suite in `build_expectation_suite()` does not validate country codes, so that row is not caught by the defined suite.

Because any row with at least one violation is quarantined without double counting the row, the 8 detected violations isolate exactly **6 unique rows** (rows 164, 251, 282, 344, 420, 551), leaving 594 clean rows.
