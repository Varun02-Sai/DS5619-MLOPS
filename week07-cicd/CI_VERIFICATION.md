# CI verification

Fill this in after you push and watch the workflow run on GitHub (Actions
tab of your repo). This is how we confirm your CI actually ran green in a
real GitHub Actions runner, not just locally.

## Workflow run

Paste the URL of a successful run of all three jobs (Actions tab -> click
the run -> copy the URL):

```
https://github.com/Varun02-Sai/DS5619-MLOPS/actions/runs/18029340921
```

## Job summary

For each job, note pass/fail and how long it took:

- `lint`: pass (18s)
- `unit-test`: pass (22s)
- `integration-test`: pass (51s)

## What broke on the way there (optional but useful)

Forgot to make `integration_test.sh` executable at first so the runner threw permission denied. Added `chmod +x` before running the script and it passed.
