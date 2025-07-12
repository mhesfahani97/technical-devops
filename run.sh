#!/bin/bash

# application code is 8000, I used 8000 in Dockerfile too.
uvicorn devops_interview.main:app --reload --host 0.0.0.0 --port 5000
