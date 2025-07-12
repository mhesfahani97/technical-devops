#!/bin/bash

uvicorn devops_interview.main:app --reload --host 0.0.0.0 --port 5000
