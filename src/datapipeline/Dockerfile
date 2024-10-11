FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile

CMD ["/bin/bash"]