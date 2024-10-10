FROM python:3.11-slim-buster

ENV PYENV_SHELL=/bin/bash

RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential git && \
    pip install --no-cache-dir --upgrade pip && \
    pip install pipenv && \
    useradd -ms /bin/bash app -d /home/app -u 1000 -p "$(openssl passwd -1 Passw0rd)"

USER app
WORKDIR /app

ADD . /app

RUN pipenv lock && pipenv sync

ENTRYPOINT ["/bin/bash"]

CMD ["-c", "pipenv shell"]
