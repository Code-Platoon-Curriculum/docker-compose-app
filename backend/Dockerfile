# Use python base image, it uses some sort linux
FROM python:3.11-buster

# all our other dockerfile commands will be executed from this dir
WORKDIR /src

# copy requirements.txt from host filesystem and use it to install python dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy the entire source code from our project dir
COPY . .

# expose the port django listens for requests on
EXPOSE 8000

# start django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
