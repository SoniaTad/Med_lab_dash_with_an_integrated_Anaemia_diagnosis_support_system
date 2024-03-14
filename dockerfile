FROM python:3.12-slim 
## this is to containerize the practical django project 



WORKDIR /code

COPY ./MarengoLab /code/
RUN apt-get update && apt-get install -y build-essential gcc pkg-config libmariadb-dev
RUN pip install --no-cache-dir -r requirements.txt