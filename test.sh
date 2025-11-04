#!/bin/bash
set -e

case "$1" in
  base)
    # Run existing test suite; should pass on the base commit
    pytest tests/ -v
    ;;
  new)
    # Run only the newly added tests; expected to fail before implementing the feature
    pytest tests/tests_select_operation.py -v
    ;;
  *)
    echo "Usage: ./test.sh {base|new}"
    exit 1
    ;;
esac
