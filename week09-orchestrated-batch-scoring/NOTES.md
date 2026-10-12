# NOTES.md — Week 9: Orchestrated Batch Scoring

**Student ID used with `generate_for_student.py`:**
142301040


## notify retry count

It took 3 attempts (failed twice on transient errors, then succeeded on the 3rd attempt, as recorded in dag_run_summary.json).


## Branch independence

`load` only depends on `score`, not on `notify`. In the execution order, `load` finished before `notify` was called. Even if the order differed, independent branches in a DAG shouldn't block each other. A failure or retry in one task shouldn't stop unrelated downstream tasks that don't depend on it.


## Retry cost under FinOps

If each attempt is a paid metered API call, I would not retry every error blindly. I would only retry transient issues (like rate limits or 503 timeouts) using exponential backoff, and fail fast on permanent 4xx errors. Retrying every task the same way is risky because retrying non-recoverable errors or expensive compute jobs wastes money without solving the failure.
