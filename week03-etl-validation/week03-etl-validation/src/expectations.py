"""
A minimal, from-scratch expectations framework in the spirit of Great
Expectations / data contracts (this week's lecture). You are implementing
the checking logic yourself rather than importing a library — the goal is
to understand what these tools actually do under the hood.

Fill in the four functions marked # TODO. Do not change the Violation
dataclass or any function signature.
"""
from dataclasses import dataclass


@dataclass
class Violation:
    expectation: str
    column: str
    row_index: int
    detail: str


def _is_null(value):
    return value is None or (isinstance(value, str) and value.strip() == "")


def expect_column_not_null(rows, column):
    """Return a Violation for every row where rows[i][column] is null/empty."""
    violations = []
    for i, row in enumerate(rows):
        val = row.get(column)
        if _is_null(val):
            violations.append(Violation("expect_column_not_null", column, i, "null or empty value"))
    return violations


def expect_column_positive(rows, column):
    """Return a Violation for every row where rows[i][column], cast to float,
    is not strictly greater than 0. If the value can't be cast to float at
    all, that also counts as a violation (detail should say so).
    """
    violations = []
    for i, row in enumerate(rows):
        val = row.get(column)
        if _is_null(val):
            violations.append(Violation("expect_column_positive", column, i, "null value"))
            continue
        try:
            num = float(val)
            if num <= 0:
                violations.append(Violation("expect_column_positive", column, i, "value not positive"))
        except (ValueError, TypeError):
            violations.append(Violation("expect_column_positive", column, i, "cannot convert to float"))
    return violations


def expect_column_in_set(rows, column, allowed_values):
    """Return a Violation for every row where rows[i][column] is not a member
    of allowed_values (a set or list you're given).
    """
    violations = []
    allowed = set(allowed_values)
    for i, row in enumerate(rows):
        val = row.get(column)
        if val not in allowed:
            violations.append(Violation("expect_column_in_set", column, i, "value not in allowed set"))
    return violations


def expect_column_unique(rows, column):
    """Return a Violation for every row AFTER THE FIRST that repeats a value
    already seen in `column`. (i.e. if three rows share a value, rows 2 and 3
    are violations; row 1 is not.)
    """
    violations = []
    seen = set()
    for i, row in enumerate(rows):
        val = row.get(column)
        if val in seen:
            violations.append(Violation("expect_column_unique", column, i, "duplicate value"))
        else:
            seen.add(val)
    return violations
