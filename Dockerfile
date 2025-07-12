FROM docker.arvancloud.ir/python:3.13

WORKDIR /app

COPY devops_interview .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["uvicorn", "devops_interview.main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]

