#!/bin/bash


# Instead of a .env file we create our env files here
# These are the config settings for our system


# Django config
# One way to keep env vars out of version control is put all the export env var statements
# in a different shell script, run it like below, and use gitignore to ignore that shell script
source "./make-secret-env-vars.sh"

echo "secret env var is: $MY_SECRET_ENV_VAR"

## Django General config
export SECRET_KEY="20b)-+*r&ci!f_wz+*q^4cvb8!*9rh+r9=d1x!q551os%tu@hf"
export DEBUG=True
export STATIC_URL="static/"

## Django Networking config
export ALLOWED_HOSTS="*"

## Django DB config
## ALSO USED FOR POSTGRES CONFIG IN docker-compose.yml
export DB_NAME=wines
export DB_USER=postgres
export DB_PASSWORD=postgres
export DB_PORT=5432 #TODO: Delete, postgres image doesnt allow
export DB_HOST=db # this comes from the docker-compose.yml


# Create and Run docker containers using our env vars
# --build forces a new build of images every time this is run
# THIS IS A GOOOD THING
docker-compose -f docker-compose.dev.yml up -d --build

# make sure postgres container is ready then apply migrations
sleep 10
docker exec docker-compose-app-api-1 python /src/manage.py makemigrations
docker exec docker-compose-app-api-1 python /src/manage.py migrate