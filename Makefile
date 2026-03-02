lint:
	uv run ruff check --fix --exit-zero
	uv run ruff format