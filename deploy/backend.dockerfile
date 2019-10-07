FROM python:stretch

RUN apt-get update && apt-get install -y --no-install-recommends \
                mysql-client

COPY . /opt/app

WORKDIR /opt/app

RUN pip install -r deploy/requirements.txt

CMD ["sh", "/opt/app/deploy/entrypoint.sh"]
