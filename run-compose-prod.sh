#!/bin/sh

###
# This script takes command line args and uses them to create the env vars
# needed by docker/docker-compose, and then spins up the docker containers, etc.
#
# Useage: ./run-compose-prod.sh <MY_SECRET_KEY> <DEBUG> <POSTGRES>DB> <POSTGRES_USER> <POSTGRES_PASSWORD> <VERSION> 
# ./run-compose-prod
###

# IMPORTANT: You will need to set this to your dockerhub username
# The Dockerhub account where the images are stored
export DOCKERHUB_UNAME=chadmowbray

# These environment variables come from command line arguments.
# They are consumed by the docker-compose file.
export SECRET_KEY=$1
export DEBUG=$2
export POSTGRES_DB=$3
export POSTGRES_USER=$4
export POSTGRES_PASSWORD=$5
export NEW_VERSION=$6

docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d

# make sure the postgres container is ready, then run migrations
sleep 10 
docker exec ec2-user-api-1 python /src/manage.py makemigrations 
docker exec ec2-user-api-1 python /src/manage.py migrate
