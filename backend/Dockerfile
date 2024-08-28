FROM python:3.11-buster

WORKDIR /src
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# start django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

