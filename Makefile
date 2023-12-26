format:
	black abc/
	black tests/
	ruff format abc/
	ruff format tests/

lint:
	black --check abc/
	black --check tests/
	ruff check abc/
	ruff check tests/
