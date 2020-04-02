build: get_docker
	docker-compose -f docker-compose.prod.yml up --build -d
get_docker:
	@echo "Getting Docker"
	#[ -z `dpkg -l | grep docker` ] && sudo apt-get install docker

clean:
	@echo "Cleaning up"
	docker-compose down -v