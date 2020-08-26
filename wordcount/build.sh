#!/bin/bash

# Run locally: gunicorn --log-config ./config/gunicorn_logging.conf --config ./config/gunicorn_config.py api:app
# Run docker locally: docker run -p 4000:8080 imagefetcherapi:latest

# customer_care_api_runmode can be development, qa, or production...
#docker build --no-cache \
docker build \
	--build-arg aws_access_key_id=$AWS_ACCESS_KEY_ID \
	--build-arg aws_secret_access_key=$AWS_SECRET_ACCESS_KEY \
	--build-arg aws_default_region=$AWS_DEFAULT_REGION \
	--build-arg bucket=testupload01 \
	--build-arg region=us-east-1 \
	--build-arg inputkey=input.txt \
	--build-arg outputkey=output.txt \
	-t wordcount .
