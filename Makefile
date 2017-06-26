bash:
	docker-compose build former
	docker-compose run former bash

test:
	py.test --cov=former tests

release-pip:
	rm -fr dist
	rm -f README.rst
	pandoc --from=markdown --to=rst --output=README.rst README.md
	rm -fr dist
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr dist

CONTAINER=flomotlik/former

release-docker:
	docker build -t $(CONTAINER) -f Dockerfile.release --no-cache .
	docker push $(CONTAINER)

release: release-pip release-docker