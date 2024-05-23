ARG PYTHON_VERSION=3.11.7
FROM python:${PYTHON_VERSION}-slim as base

LABEL org.opencontainers.image.source=https://github.com/yudiz-solutions/interactive-chatbot-python-backend

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    apt-get update && apt-get install nano \
    && apt-get install gcc python3-dev -y \
    && apt-get install -y sudo \
    && python -m pip install -r requirements.txt


COPY . .
