test:
	py.test tests --cov pyger --cov-report term-missing

flake:
	flake8 pyger
