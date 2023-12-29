format:
	black aic/
	black tests/
	ruff format aic/
	ruff format tests/

lint:
	black --check aic/
	black --check tests/
	ruff check aic/
	ruff check tests/
