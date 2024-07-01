FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /app

EXPOSE 5000

RUN useradd -s /usr/sbin/nologin user \
    && mkdir /upload && chown user:user /upload && chmod 1777 /upload

VOLUME /upload

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=./requirements.txt,target=requirements.txt \
    pip install --disable-pip-version-check -r requirements.txt

COPY ./uploader ./uploader

USER user

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--worker-class", "gevent", "uploader:app"]
