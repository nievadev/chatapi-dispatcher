tests:
	@python -m unittest discover

dev:
	@uvicorn src.main:app --reload

coverage:
	@python -m pytest --cov=. --cov-report term-missing

check:
	@mypy .
	@flake8 .
	@pylint src
