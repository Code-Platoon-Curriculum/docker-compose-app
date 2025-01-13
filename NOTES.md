# Dockerizing the Frontend

- Set up CORS:
  - in Django code
  - setting CORS env vars in docker-compose and shell script

- Identify frontend config settings that need to be env vars
  - VITE_BASE_URL

> *IMPORTANT:*  frontend env vars must be set in the nginx Dockerfile, because we need them during the *image build step,* as that is when vite needs them in order to inject them in the `dist/` js bundle. Docker compose env vars are only set during the *run* step when a container runs the built image.

- Create nginx dockerfile
  - create nginx config
    - Map http requests with `api/`  in the URL to go to django api

- Update docker-compose and shell script