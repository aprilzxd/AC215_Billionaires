FROM python:3.11-slim

ENV PYENV_SHELL=/bin/bash

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv

RUN pipenv lock && pipenv sync

COPY . /app

ENTRYPOINT ["/bin/bash"]

CMD ["-c", "pipenv shell"]
