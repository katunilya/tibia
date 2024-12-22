PYTHON_VERSION = 3.12

.PHONY: setup format lint test test-debug

setup:
	pyenv local ${PYTHON_VERSION}
	poetry env use ${PYTHON_VERSION}
	poetry install --no-root
	poetry run pre-commit install --hook-type pre-commit --hook-type commit-msg

format:
	poetry run ruff format

lint:
	poetry run ruff check

test:
	poetry run pytest --cov $(arg) -k "$(k)"

test-debug:
	poetry run pytest --showlocals --tb=long --log-cli-level=DEBUG --vv
