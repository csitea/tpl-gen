.PHONY: do-prune-docker-system ## @-> 00.01 stop & completely wipe out all the docker caches for ALL IMAGES !!!
do-prune-docker-system:
	@clear

	@if [ "$$(docker ps -q)" != "" ]; then \
		docker kill $$(docker ps -q); \
		docker rm $$(docker ps -aq)
	fi
	@if [ $$(docker volume ls -q|wc -l) > 0 ]; then \
		docker volume rm $(docker volume ls -q); \
	fi

	docker image prune -a -f
	docker builder prune -f -a
	docker system prune --volumes -f
	sudo rm -rf /var/lib/docker/*
