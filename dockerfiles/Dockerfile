FROM python:3.6-alpine3.10
RUN python --version
RUN apk update \
    && apk upgrade \
    && apk add git
RUN pip install prancer-basic
RUN git --version