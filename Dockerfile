FROM ubuntu

RUN apt-get update && apt-get -y install python3.7 python3-pip python3-dev libpq-dev gcc locales
RUN locale-gen en_US.UTF-8
COPY . /opt/source-code
RUN pip3 install -r /opt/source-code/requirements.txt
EXPOSE 5000
ENV LC_ALL en_US.utf-8
ENV LANG en_US.utf-8
ENV FLASK_APP /opt/source-code/app.py 

ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]