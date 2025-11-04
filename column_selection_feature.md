# Column Selection/Projection Feature

## Problem Brief

Build a column selection feature for the `rows` library that allows users to extract specific columns from tables, similar to SQL's `SELECT col1, col2` operation. This feature should work both programmatically via a Python function and through a CLI command.

The outcome is a flexible way to reduce table width by selecting only needed columns, useful for data transformation pipelines and CSV manipulation.

## Agent Instructions

1. **Implement `rows.operations.select(table, columns)` function:**
   - Accept a Table object and a list of column names
   - Validate that all requested columns exist (raise ValueError if not)
   - Return a new Table with only the selected columns in the specified order
   - Preserve field types from the original table
   - Support all table modes (eager, stream, incremental, flexible)
   - Handle empty columns list with appropriate error

2. **Add `rows select` CLI command:**
   - Command signature: `rows select COLUMNS SOURCE DESTINATION`
   - COLUMNS: comma-separated list of column names (e.g., "name,age,city")
   - Support standard options: input/output encoding, locale, order-by, verify-ssl
   - Validate columns exist in source table before processing
   - Export result to destination with proper encoding/format
   - Follow existing CLI patterns (use Click decorators, _import_table helper)

3. **Export the function:**
   - Add `select` to `rows/__init__.py` imports
   - Ensure `rows.select` is accessible alongside `rows.join`, `rows.transform`, etc.

4. **Acceptance criteria:**
   - All new tests pass
   - Existing tests remain passing
   - CLI command works with CSV, JSON, and other supported formats
   - Column order matches requested order
   - Field types are preserved correctly

## Test Assumptions

- Function: `rows.operations.select(table, columns)` where columns is a list
- Import: `rows.select` should be available
- CLI: `rows select column1,column2 input.csv output.csv`
- Errors: ValueError raised for missing/empty columns
