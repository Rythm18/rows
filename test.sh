#!/bin/bash
set -e

# Find pytest in common locations
PYTEST=$(command -v pytest || echo "/home/ubuntu/.local/bin/pytest")

case "$1" in
  base)
    # Run existing test suite; should pass on the base commit
    $PYTEST tests/ rows/ --doctest-modules --ignore=to-do/ --ignore=examples/ --ignore=rows/plugins/__init__.py
    ;;
  new)
    # Run only the newly added tests; expected to fail before implementing the feature
    $PYTEST tests/tests_operations_union.py -v
    ;;
  *)
    echo "Usage: ./test.sh {base|new}"
    exit 1
    ;;
esac
