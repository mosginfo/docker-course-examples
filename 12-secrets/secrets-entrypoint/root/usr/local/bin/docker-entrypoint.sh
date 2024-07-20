#!/usr/bin/env sh

# Как только любая команда вернётся с ненулевым кодом возврата - выйти
set -e

# Подключаем библиотеку для работы с секретами
. secrets.sh

# Пересоздаем все указанные переменные окружения
# Любая переменная может быть передана как секрет с суффиксом _FILE в имени
# Все переменные, кроме MONGO_HOST, обязательные для указания
fileEnv 'MONGO_HOST' 'mongo'
fileEnv 'MONGO_USERNAME'
fileEnv 'MONGO_PASSWORD'
fileEnv 'MONGO_DATABASE'


# Используем скрипт/программу для проверки минимальной версии PHP
if compver.sh "$PHP_VERSION < 8.0"; then
    echo "Not supported PHP version $PHP_VERSION, required version >= 8.0"
    exit 1
fi


# Выполняем "родительский" скрипт с переданными аргументами
exec docker-php-entrypoint "$@"
