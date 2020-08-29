#!/bin/bash

sam local invoke \
   --event event.json \
   --template ../../template.yaml \
   --env-vars env.json \
   --region us-east-1
