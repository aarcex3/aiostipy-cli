# Variables
#PYTHON := poetry run python
PYTEST := poetry run pytest
BLACK := poetry run black
FIND := find

# Directories
SRC_DIR := ./src
TEST_DIR := ./tests

# Targets
.PHONY: clean test run



#Format the files
format:
	$(BLACK) $(SRC_DIR)

# Clean target to delete __pycache__ directories
clean:
	$(FIND) . -type d -name "__pycache__" -exec rm -rf {} +

# Test target to run pytest with specified options
test:
	$(PYTEST) $(TEST_DIR) -vv -s --showlocals

