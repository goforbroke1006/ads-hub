.PHONY: docker
docker:
	docker-compose build
	docker-compose down
	docker-compose up -d

dep:
	pip install --user -r requirements.txt