FROM python:stretch

RUN apt-get update && apt-get install -y --no-install-recommends \
                mysql-client

COPY . /opt/app
RUN mkdir -p /root/.credentials
WORKDIR /opt/app
COPY deploy/gmail-credentials.json /root/.credentials/gmail-credentials.json
RUN pip install -r deploy/requirements.txt
RUN python -m spacy download en_core_web_md

CMD ["sh", "/opt/app/deploy/entrypoint.sh"]
