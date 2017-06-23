bash:
	docker-compose build former
	docker-compose run former bash

test:
	py.test --cov=former tests