# NOTES.md — Week 2: Config-Driven Data Pipelines

**Student ID used with `generate_for_student.py`:**
142301040


## What was hardcoded, and what would switching it have required?

In the original code, the `INPUT_PATH`, `HIGH_VALUE_THRESHOLD`, and `OUTPUT_PATH` were hardcoded values. Also, the `load_csv()` function was hardcoded to only work for CSVs. If I wanted to change the threshold or switch to JSON, I would have had to manually edit the `pipeline_hardcoded.py` file and redeploy the code.
