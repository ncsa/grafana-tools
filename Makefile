dev:
	bash dev.sh

# cmdline-build:
# 	docker-compose -f build.yaml build
# 	docker-compose -f build.yaml run gunicorn_project bash

clean:
	docker compose down
	docker compose rm -f
	docker container prune -f
	docker images | awk '/grafana_api/ {print $$3}' | xargs -r docker rmi
	docker system prune -f
