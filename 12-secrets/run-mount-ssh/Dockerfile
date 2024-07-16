FROM node:20.14-bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# /var/cache/apt - кеш загруженных пакетов
# /var/lib/apt - метаданные о пакетах
# sharing=locked - кэш будет синхронизирован между сборками и не будет конфликтовать при параллельных запусках
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    # Эта команда удаляет файл конфигурации docker-clean,
    # который по умолчанию удаляет загруженные пакеты, чтобы уменьшить размер образа
    # Удаление этого файла позволяет сохранить кэш загруженных пакетов
    rm -f /etc/apt/apt.conf.d/docker-clean; \
    # Эта команда создает новый файл конфигурации keep-cache, в который добавляется директива,
    # указывающая apt сохранять загруженные пакеты после установки
    # Это помогает использовать эти пакеты в последующих сборках образа,
    # тем самым уменьшая время установки при повторных сборках
    echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache \
    && apt update && apt install -yq --no-install-recommends \
        openssh-client \
        git \
    && mkdir -p -m 0700 ~/.ssh \
    && ssh-keyscan github.com >> ~/.ssh/known_hosts

# id        Идентификатор сокета агента SSH или ключа (по умолчанию "default")
# target    Путь к сокету агента SSH (по умолчанию /run/buildkit/ssh_agent.${N})
# required  Если установлено в true, команда завершится ошибкой, если ключ недоступен (по умолчанию false)
# mode      Права доступа для сокета в восьмеричной системе (по умолчанию 0600)
# uid       Идентификатор пользователя для сокета (по умолчанию 0)
# gid       Идентификатор группы для сокета (по умолчанию 0)
RUN --mount=type=ssh,required \
    npm i git+ssh://git@github.com:kyzima-spb/api-call-simplifier.git#v0.2.1
