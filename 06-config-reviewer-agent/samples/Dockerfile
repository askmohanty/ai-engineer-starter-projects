FROM python:latest

ENV DATABASE_PASSWORD=SuperSecret123

RUN apt-get update
RUN apt-get install -y curl vim build-essential

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000
CMD python app.py
