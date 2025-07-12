FROM docker.arvancloud.ir/python:3.13

WORKDIR /app

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main

COPY devops_interview /app/devops_interview

EXPOSE 8000

# the port in application code is 8000, I used 8000 in Dockerfile too.
CMD ["uvicorn", "devops_interview.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

