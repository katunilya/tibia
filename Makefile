.PHONY: setup format test test-debug

setup:
	pyenv local 3.12
	poetry env use 3.12
	poetry install --no-root

format:
	poetry run ruff format

test:
	poetry run pytest \
		--cov \
		$(arg) \
		-k "$(k)"

test-debug:
	poetry run pytest \
		--showlocals \
		--tb=long \
		-vvv
