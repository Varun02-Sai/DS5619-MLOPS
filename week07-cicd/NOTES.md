# NOTES.md — Week 7: CI/CD Integration Testing

**Student ID used with `generate_for_student.py`:**
142301040


## Why gate integration-test on needs: [lint, unit-test]?

Linting and unit tests only take a few seconds, while building and running the Docker container takes about a minute. If there is a simple syntax error or a failing test, running the container test in parallel would just waste runner minutes and time building an image that we already know is broken. Gating it with `needs:` stops the pipeline early so we don't spend CI minutes building broken code.
