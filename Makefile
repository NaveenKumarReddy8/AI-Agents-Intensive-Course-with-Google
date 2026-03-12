lint:
	uv run ruff check --fix --select ALL --exit-zero
	uv run ruff format