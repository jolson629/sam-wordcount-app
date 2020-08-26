#!/bin/bash

# Can configure at Docker build time, if needed.
#exec pipenv run python brute_force_wc.py --bucket testupload01 --region us-east-1 --inputKey input.txt --outputKey output.txt
exec pipenv run python brute_force_wc.py 
