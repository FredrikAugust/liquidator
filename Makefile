clean:
		@rm -fr `find . -name __pycache__`

test:
		@pytest -v server/tests --cov-report term-missing --cov=liquidator_server

