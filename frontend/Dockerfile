FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install django pymongo requests
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]