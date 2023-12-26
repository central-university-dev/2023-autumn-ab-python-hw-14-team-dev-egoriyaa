format:
	black src/
	black tests/
	ruff format src/
	ruff format tests/

lint:
	black --check src/
	black --check tests/
	ruff check src/
	ruff check tests/
