# A Containerized React and Django Rest Framework Deployment

## Overview


## How to Use This
As you can see there are three folders in this repo:
- `/backend` has your DRF application, along with its corresponding Dockerfile.
- `/frontend` has your React application.
- `/webserver` has a configuration file for your nginx server and the Dockerfile that builds your React code and configures the server.

The rest of the files at the project's root are for putting everything together.  The centerpiece is the [docker-compose](https://docs.docker.com/compose/gettingstarted/) file (in both a development and production version).

Our application has three "services" in docker-compose lingo.  A service is basically a container.  I've somewhat arbitrarily called the DRF container "api", and the React/nginx one "nginx".  The `build` key (and its sub-keys) just tell docker-compose where the Dockerfile is.  So in the case of `docker-compose.dev.yml`, the Dockerfile for "api" is in the `/backend` folder.  It's smart enough to find the Dockerfile in there.  Everything else is optional configuration.  docker-compose uses that configuration to run your image.

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

The other `.sh` scripts are conveniences for running the docker-compose files.
NOTE: You might have to change the file permissions to run the scripts `chmod 755 myscript.sh`.

`run-compose-dev.sh` sets some environment variables used in the docker-compose file, then calls `docker-compose -f docker-compose.dev.yml up`.  "up" starts everything (this might take a while).  And when you're done, you just run `docker-compose -f docker-compose.dev.yml down` (not part of a script, but you can add your own, or maybe a [Makefile](https://medium.com/freestoneinfotech/simplifying-docker-compose-operations-using-makefile-26d451456d63) if you really want to go all out).

Lastly, `build-and-push-images.sh` (which takes two arguments: your EC2 IP address, and the current version of your application, i.e. 1.2) is for pushing up your images to Dockerhub so they can be accessed for the production deployment.  Be sure to set the `DOCKERHUB_UNAME` variable to your own Dockerhub account. Versioning your containers enables you to keep track of what you have deployed at any given time.


## Development

The main difference between the `docker-compose.dev.yml` and `docker-compose.prod.yml` files is that the dev version uses local Dockerfiles to build everything, whereas the prod version uses images that have been pushed to your Dockerhub account (and versioned).

## Production

1. Create an EC2 instance.

2. Get the `pem` keyfile for your ec2 and save it to your machine

3. ssh into your EC2 using the `pem` keyfile

4. Copy over files to the EC2 you will need with `scp` (very similar to ssh):

```bash
scp  -i "<MY_PEM_KEY_FILENAME>" ./setup-ec2.sh ./run-compose-prod.sh ./docker-compose.prod.yml   <MY_EC2_USERNAME>@<MY_EC2_IP_ADDR>.compute-1.amazonaws.com:/home/<MY_EC2_USERNAME>
```

Example running the scp command (your filenames, etc will be different):

```bash
scp  -i "vanillaApp.pem" ./setup-ec2.sh ./run-compose-prod.sh ./docker-compose.prod.yml   ec2-user@ec2-18-234-99-58.compute-1.amazonaws.com:/home/ec2-user
```

5. Run the setup ec2 shell script on the EC2. This installs docker, docker-compose, etc, and configures docker stuff on the ec2:

```bash
./setup-ec2.sh
```

6. Keep the EC2 running so the IP does not change. 

7. **On your local machine**, not the EC2, run the `build-and-push` images shell script. Run it like so with the following arguments:
`build-and-push-images.sh <MY_EC2_IP_ADDR> <VERSION>` where `<VERSION>` the version of your app (you get to set this, 1, 2, 3, etc).

8. In `run-compose-prod.sh` modify it to use your dockerhub username. Be sure to review the documentation comments in the file, which have instructions.

9. Now, on your EC2 run `run-compose-prod.sh` and pass your env var settings as arguments (see the file). Example:

19. Run `docker ps` to confirm your containers are up and running!!

You can use `stop-compse-prod.sh` to stop all the containers, or docker/docker compose to stop individual containers as neeed.