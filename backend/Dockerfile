
FROM python:3.11

WORKDIR .

COPY ./requirements.txt ./requirements.txt

RUN apt update

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

#CMD ["gunicorn", "main:app", "--workers" ,"4" ,"--worker-class" ,"uvicorn.workers.UvicornWorker", "--bind" ,"0.0.0.0:80"]