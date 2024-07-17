FROM php:8.3-apache

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
        libssl-dev \
        libsasl2-dev \
    && pecl install mongodb \
    && docker-php-ext-enable mongodb

COPY ./index.php ./
