FROM node:20.14-bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache \
    && apt update && apt install -yq --no-install-recommends \
        # для работы с ssh нужен клиент
        openssh-client \
        # пакет git нужен для установки из git репозитория
        git \
        # можно ставить npm-пакеты из публичных репозиториев по http(s)
        # ca-certificates нужен, чтобы избежать ошибки с сертификатами
        ca-certificates \
    && mkdir -p -m 0700 ~/.ssh \
    && ssh-keyscan github.com >> ~/.ssh/known_hosts

# id        Идентификатор сокета агента SSH или ключа (по умолчанию "default")
# target    Путь к сокету агента SSH (по умолчанию /run/buildkit/ssh_agent.${N})
# required  Если установлено в true, команда завершится ошибкой, если ключ недоступен (по умолчанию false)
# mode      Права доступа для сокета в восьмеричной системе (по умолчанию 0600)
# uid       Идентификатор пользователя для сокета (по умолчанию 0)
# gid       Идентификатор группы для сокета (по умолчанию 0)
RUN --mount=type=ssh,required \
    npm i git+ssh://@github.com:kyzima-spb/kirill-vercetti-npm-package.git#v1.0.0
