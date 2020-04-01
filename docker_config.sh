#!/bin/bash
echo Running
#docker build . -t rorbachg/rest-api-example
#docker run -it rorbachg/rest-api-example
#docker run -p 5000:5000 -w="/opt/source-code" rorbachg/rest-api-example
docker-compose rm -fs
#docker-compose up --build
docker-compose -f docker-compose.prod.yml up --build 