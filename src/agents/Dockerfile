FROM python:3.11-slim-buster

RUN set -ex; \
    pip install --no-cache-dir --upgrade pip && \
    pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --deploy --ignore-pipfile

COPY . /app

EXPOSE 8501

ENTRYPOINT ["/bin/bash"]

