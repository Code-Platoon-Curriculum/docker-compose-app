# This is the 'builder pattern' in DOcker
# 1. Build the production react app
# 2. Take that build, stick it in the nginx docker image, and, get rid of stuff we no longer need, like:
#    - node.js
#    - src/
#    - node_modules/

FROM node:lts-alpine as builder

WORKDIR /frontend

# Set env vars when we build the image, AND, when we run run the container.
# We cannot do this in docker-compose because docker-compose environment vars 
# get set when the container is  *run*, not during the *image build step* which is when vite/react.js needs them.
# See https://stackoverflow.com/a/58579325
ARG VITE_BASE_URL=localhost
ENV VITE_BASE_URL=$VITE_BASE_URL

COPY ./frontend/package.json .
RUN npm install
COPY ./frontend .
RUN npm run build

# This is the final image we want, we can throw away
# everything except dist/ 

FROM nginx:alpine

COPY ./webserver/default.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /frontend/dist /usr/share/nginx/html
