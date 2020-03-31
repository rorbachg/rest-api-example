#!/bin/bash

docker build . -t rorbachg/rest-api-example
docker run -p 5000:5000 --name rest_api rorbachg/rest-api-example