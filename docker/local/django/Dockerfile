ARG PYTHON_VERSION=3.9-slim-bullseye

FROM python:${PYTHON_VERSION} AS python



FROM python AS python-build-stage
ARG BUILD_ENVIRONMENT=local

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev

COPY ./dynamic-blog-api/requirements .

RUN pip wheel --wheel-dir /usr/src/app/wheels \
    -r ${BUILD_ENVIRONMENT}.txt



FROM python AS python-run-stage
ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=False \
    && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage /usr/src/app/wheels /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/


COPY ./dynamic-blog-api ${APP_HOME}

ADD ./docker/local/django/entrypoint ./entrypoint
RUN sed -i 's/\r$//g' ./entrypoint
RUN chmod +x ./entrypoint

ADD ./docker/local/django/start ./start
RUN sed -i 's/\r$//g' ./start
RUN chmod +x ./start

ADD ./docker/local/django/celery/worker/start-celeryworker ./start-celeryworker
RUN sed -i 's/\r$//g' ./start-celeryworker
RUN chmod +x ./start-celeryworker

ADD ./docker/local/django/celery/flower/start-flower ./start-flower
RUN sed -i 's/\r$//g' ./start-flower
RUN chmod +x ./start-flower

ENTRYPOINT ["./entrypoint"]

