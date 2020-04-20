FROM python:3.6-alpine3.10
RUN python --version
RUN apk update \
    && apk upgrade \
    && apk add git build-base libffi-dev openssl-dev
RUN pip install ply    
RUN pip install prancer-basic
