FROM python:3.10.13-alpine@sha256:d75c7712b6161e93efa287df5fceedeaeeb2ef773f44a6b71efc6e42fec4666d
ARG APP_VERSION
ENV APP_VERSION=$APP_VERSION
RUN apk update \
    && apk upgrade \
    && apk add git build-base libffi-dev openssl-dev
RUN pip install --no-cache-dir ply
RUN pip install --no-cache-dir prancer-basic==$APP_VERSION
