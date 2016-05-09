FROM docker:1.11.1
RUN apk update && apk add python py-pip bash python-dev
RUN pip install docker-compose
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/