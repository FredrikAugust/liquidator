clean:
        @rm -fr `find . -name __pycache__`


test:
        @pytest -q server/tests

