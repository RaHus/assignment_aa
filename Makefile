dev-install:
	[[ -z $VIRTUAL_ENV ]] && echo not a virtualenv && exit 1
	pip install -e .[dev,testing]
install:
	pip install -e .
egg:
	python setup.py bdist_egg
test:
	py.test --cov=assignment_aa --cov-report=term-missing -s
push:
	git push -u origin master
docs:
	echo "ToDo"
