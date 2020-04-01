FROM python:3.6.7

COPY ./requirements.txt /opt/source-code/requirements.txt
RUN pip3 install -r /opt/source-code/requirements.txt

ENV FLASK_APP /opt/source-code/app.py
ENV FLASK_RUN_HOST 0.0.0.0
COPY . /opt/source-code
WORKDIR /opt/source-code