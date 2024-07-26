FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1

# id        Идентификатор секрета (по умолчанию basename для пути target)
# target    Путь монтирования (по умолчанию /run/secrets/ + id)
# required  Если установлено в true, команда завершится ошибкой, если секрет недоступен (по умолчанию false)
# mode      Права доступа для файла секрета в восьмеричной системе (по умолчанию 0400)
# uid       Идентификатор пользователя для файла секрета (по умолчанию 0)
# gid       Идентификатор группы для файла секрета (по умолчанию 0)
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=secret,id=indexurl,target=/root/.indexurl,required \
    pip install \
        --disable-pip-version-check \
        --index-url "$(cat /root/.indexurl)" \
        # будет ошибка, если не добавить хост в доверенные
        # разбиваем по @ адрес и вытаскиваем последний компонент - хост:порт
        --trusted-host "$(cat /root/.indexurl | awk -F'@' '{ printf $NF }')" \
            kirill-vercetti-example-package
