
FROM python:3.11.3-bullseye

RUN mkdir -p /home/api

WORKDIR /home/api

COPY . /home/api

RUN apt update

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80

#CMD ["gunicorn", "main:app", "--workers" ,"4" ,"--worker-class" ,"uvicorn.workers.UvicornWorker", "--bind" ,"0.0.0.0:80"]