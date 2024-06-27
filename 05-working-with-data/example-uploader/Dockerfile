FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /app

EXPOSE 5000

RUN useradd -s /usr/sbin/nologin user

COPY ./requirements.txt .

RUN pip install \
        --no-cache-dir \
        --disable-pip-version-check \
        -r requirements.txt \
    && mkdir /upload && chown user:user /upload && chmod 1777 /upload

VOLUME /upload

COPY . .

USER user

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--worker-class", "gevent", "app:app"]
