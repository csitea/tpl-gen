.PHONY: do-prune-docker-system ## @-> 00.01 stop & completely wipe out all the docker caches for ALL IMAGES !!!
do-prune-docker-system:
	@clear
	docker kill $$(docker ps -q)
	docker rm $$(docker ps -aq)
	docker image prune -a -f
	docker builder prune -f -a
	docker volume rm $(docker volume ls -q)
	docker system prune --volumes -f
	sudo rm -rf /var/lib/docker/*
