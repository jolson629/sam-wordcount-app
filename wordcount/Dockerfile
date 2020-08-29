FROM ubuntu:20.04

ARG aws_access_key_id
ENV AWS_ACCESS_KEY_ID=$aws_access_key_id

ARG aws_secret_access_key
ENV AWS_SECRET_ACCESS_KEY=$aws_secret_access_key

ARG aws_default_region
ENV AWS_DEFAULT_REGION=$aws_default_region

ARG inputbucket
ENV INPUTBUCKET=$inputbucket

ARG inputkey
ENV INPUTKEY=$inputkey

ARG outputbucket
ENV OUTPUTBUCKET=$outputbucket

ARG outputkey
ENV OUTPUTKEY=$outputkey

ARG region
ENV REGION=$region


RUN apt-get update
RUN apt-get install -y software-properties-common

RUN apt-get update
RUN apt-get install -y build-essential python3-pip
RUN apt-get install -y unzip

RUN mkdir -p /wordcount/
RUN mkdir -p /wordcount/log

COPY ./brute_force_wc.py /wordcount/brute_force_wc.py

COPY ./Pipfile /wordcount/Pipfile
COPY ./Pipfile.lock /wordcount/Pipfile.lock
RUN pip3 install --index-url=https://pypi.python.org/simple/ pipenv


WORKDIR /wordcount/

RUN pipenv install

COPY ./docker_entrypoint.sh /wordcount/docker_entrypoint.sh
RUN ["chmod", "+x", "/wordcount/docker_entrypoint.sh"]
ENTRYPOINT ["/wordcount/docker_entrypoint.sh"]
