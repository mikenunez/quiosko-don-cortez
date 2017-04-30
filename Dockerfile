FROM python:3.5
LABEL PROJECT="Quiosko Don Cortez"
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD ./code/requirements.txt /code/
RUN pip install -r requirements.txt
ADD ./code/ /code/