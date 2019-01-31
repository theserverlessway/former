build-dev:
	docker-compose build former

shell: build-dev
	docker-compose run former bash

test:
	py.test --cov=former tests
	pycodestyle .
	pyflakes .
	grep -r 'print(' former; [ "$$?" -gt 0 ]

clean:
	rm -fr dist build

build: clean build-dev
	docker-compose run former python setup.py sdist bdist_wheel
	docker-compose run former pandoc --from=markdown --to=rst --output=build/README.rst README.md

release-pip: clean build-dev build
	docker-compose run former twine upload dist/*

CONTAINER=flomotlik/former
build-docker:
	docker build -t $(CONTAINER) -f Dockerfile.release --no-cache .

release-docker: build-docker
	docker push $(CONTAINER)

release: release-pip release-docker
