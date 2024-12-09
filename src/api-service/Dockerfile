FROM python:3.11-slim
WORKDIR /app
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv
RUN pipenv install --system --deploy
COPY . /app
EXPOSE 8001
RUN chmod +x docker-entrypoint.sh
CMD ["./docker-entrypoint.sh"]
