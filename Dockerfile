FROM python:3.8.5
LABEL Name=insight Version=1.0
FROM python:3

RUN mkdir /insight
WORKDIR /insight
ADD requirements.txt /insight/
RUN pip install -r requirements.txt
EXPOSE 8500

