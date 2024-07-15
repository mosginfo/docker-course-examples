FROM python:3.12-slim-bookworm

# id        ID of the secret. Defaults to basename of the target path.
# target    Mount path. Defaults to /run/secrets/ + id.
# required  If set to true, the instruction errors out when the secret is unavailable. Defaults to false.
# mode      File mode for secret file in octal. Default 0400.
# uid       User ID for secret file. Default 0.
# gid       Group ID for secret file. Default 0.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=secret,id=indexurl,target=/root/.indexurl,required=true \
    pip install \
        --disable-pip-version-check \
        --index-url "$(cat /root/.indexurl)" \
        # будет ошибка, если не добавить хост в доверенные
        # разбиваем по @ адрес и вытаскиваем последний компонент - хост:порт
        --trusted-host "$(cat /root/.indexurl | awk -F'@' '{ printf $NF }')" \
            kirill-vercetti-example-package
