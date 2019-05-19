clean:
		@rm -fr `find . -name __pycache__`

test-server:
		cd server && tox-travis
