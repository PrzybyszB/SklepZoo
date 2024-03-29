FROM python:3.9

COPY requirements.txt /sklep-zoo/requirements.txt

WORKDIR /sklep-zoo

RUN pip3 install -r requirements.txt
RUN pip3 install mysql-connector-python

# FLASK environment settings
ENV FLASK_APP=src/__init__.py

# development ? production ? testing ?
ENV FLASK_ENV=development 
ENV FLASK_DEBUG=1

COPY src /sklep-zoo/src
COPY entrypoint.sh /sklep-zoo/entrypoint.sh
ENTRYPOINT [ "/bin/bash", "entrypoint.sh" ]

