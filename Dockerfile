FROM python:3.12.4-slim

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

RUN mkdir /app/video
RUN mkdir /app/audio

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y gcc make build-essential libssl-dev libffi-dev libpq-dev
RUN echo 'deb http://deb.debian.org/debian testing main' >> /etc/apt/sources.list
RUN apt-get install -y  ffmpeg

RUN pip install "poetry==1.3.2"
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root

COPY ./app /app

CMD ["gunicorn", "base_app.wsgi", "--bind", "0.0.0.0:8000", "-w", "1", "--reload"]
