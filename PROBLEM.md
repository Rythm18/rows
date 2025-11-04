# Table Union Operation

## Problem Brief

The rows library currently provides `join()` for horizontal table combination (merging columns) but lacks a `union()` operation for vertical combination (concatenating rows). Users need to combine multiple tables with identical schemas by stacking their rows end-to-end, similar to SQL's UNION operation. This feature enables common data pipeline tasks like merging split datasets, combining query results, or aggregating data from multiple sources.

## Agent Instructions

**Objective**: Implement a `rows.union()` function that vertically concatenates multiple tables with matching schemas.

**Acceptance Criteria**:
1. Add `union(tables)` function to `rows/operations.py` that accepts a list of Table objects
2. Validate all tables have identical field names; raise `ValueError` if schemas differ
3. Return a new Table containing all rows from all input tables in sequential order
4. Handle edge cases: empty tables (skip them), all empty tables (return empty table with first schema)
5. Export `union` from `rows/__init__.py` alongside existing operations
6. All new tests in `tests/tests_operations_union.py` must pass
7. Existing test suite must continue passing (verify with `./test.sh base`)

**Implementation Hints**:
- Follow the pattern of existing operations (`join`, `transform`, `transpose`)
- Use `create_table()` from `rows.plugins.utils` for result table creation
- Iterate through input tables, extracting rows and converting to tuples
- Preserve field types from first table's schema

## Test Assumptions

- **Function location**: `rows.operations.union(tables)`
- **Function signature**: `union(tables: List[Table]) -> Table`
- **Module export**: Accessible as `rows.union()`
- **Test file**: `tests/tests_operations_union.py`
- **Error behavior**: Raises `ValueError` with message containing "field names" when schemas mismatch
