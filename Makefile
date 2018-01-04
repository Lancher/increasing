# directories
SRC_DIR := increasing
SRC_TEST_DIR := $(SRC_DIR)/test

# *.py
SRC_TEST_PY := $(wildcard $(SRC_TEST_DIR)/*.py)
SRC_TEST_PY_MODULE := $(patsubst $(SRC_TEST_DIR)/%.py, %, $(SRC_TEST_PY))

# test
test:
	@cd $(SRC_TEST_DIR) && python -m unittest $(SRC_TEST_PY_MODULE)
