#!/bin/bash

# Can configure at Docker build time, if needed.
exec pipenv run python brute_force_wc.py 
