FROM python:3.11-slim
WORKDIR /app
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv
RUN pipenv install --system --deploy
COPY . /app
RUN chmod +x /app/docker-entrypoint.sh
EXPOSE 8001
ENTRYPOINT ["/bin/bash","./docker-entrypoint.sh"]