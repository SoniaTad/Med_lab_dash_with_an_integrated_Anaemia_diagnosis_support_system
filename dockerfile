FROM python:3.12-slim 
## this is to containerize the practical django project 


# create dir code
WORKDIR /code
# copy the whole django project folder 
COPY ./MarengoLab /code/
# install required libraries and other required package to connect to the db 
RUN apt-get update && apt-get install -y build-essential gcc pkg-config libmariadb-dev
RUN pip install --no-cache-dir -r requirements.txt