# A Containerized React and Django Rest Framework Deployment

## Overview

- The shell scripts create environment variables, execute docker compose, and run any install/setup commands.
- The docker compose files are executed by the shell scripts and use the env vars when creating images or starting containers.

## How to Use This

As you can see there are the following folders in this repo:

- `/backend` has your Django application, along with its corresponding Dockerfile.

The rest of the files at the project's root are for putting everything together.  The centerpiece is the [docker-compose](https://docs.docker.com/compose/gettingstarted/) file. 

Our application has two "services" in docker-compose lingo.  A service is basically a container.

- **"api":** Service for the Django container.
- **"db":** Service for Postgres container.

> You can name a service anything you want.

The `build` key (and its sub-keys) just tell docker-compose where the Dockerfile is.  For "api" it is in the `/backend` folder.  It's smart enough to find the Dockerfile in there.  Everything else is optional configuration.  docker-compose uses that configuration to run your image.

```yaml
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=$SECRET_KEY
      - DEBUG=$DEBUG
      - DB_NAME=$POSTGRES_DB
      - DB_USER=$POSTGRES_USER
      - DB_PASS=$POSTGRES_PASSWORD
```

is the same as

```bash
docker run -p 8000:8000 -e SECRET_KEY=$SECRET_KEY -e DEBUG=$DEBUG -e DB_NAME=$POSTGRES_DB -e DB_USER=$POSTGRES_USER -e DB_PASS=$POSTGRES_PASSWORD ./backend
```

The `docker-compose.prod.yml` is almost identical, except that it uses pre-built images stored in a Dockerhub account (so that we don't have to copy over all the source code into the EC2 instance).

The other `.sh` scripts are conveniences for running the docker-compose file.

> NOTE: You might have to change the file permissions to run the scripts `chmod 755 myscript.sh`.

`run-compose-dev.sh` sets some environment variables used in the docker-compose file, then calls `docker-compose -f docker-compose.dev.yml up`.  "up" starts everything (this might take a while).  

When you're done, just run `./stop-compose-dev.sh`. All it does is:

```bash
docker-compose -f docker-compose.dev.yml down
```
