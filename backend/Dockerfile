# Use a python base image
FROM python:3.11-buster

# All dockerfile commands will now get executed from this dir inside the docker image
WORKDIR /src

# Copy requirements.txt from host OS
COPY ./requirements.txt .

# Install django dependencies
RUN pip install -r requirements.txt

# Copy our source code from host OS into docker image
COPY . .

# Expose a port for django, so things outside docker container can access via this port
EXPOSE 8000

# start django
# IMPORTANT: Make sure the port here matches the port we EXPOSE
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 