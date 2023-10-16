FROM python:3.10.13-alpine
ARG APP_VERSION
ENV APP_VERSION=$APP_VERSION
RUN apk update \
    && apk upgrade \
    && apk add git build-base libffi-dev openssl-dev
RUN pip install ply    
RUN pip install prancer-basic==$APP_VERSION
