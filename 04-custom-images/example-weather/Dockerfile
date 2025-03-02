FROM python:3.13-slim-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=./requirements.txt,target=requirements.txt \
    pip install --disable-pip-version-check -r requirements.txt \
    && useradd -s /usr/sbin/nologin user

COPY . .

USER user

ENTRYPOINT ["python", "main.py"]
