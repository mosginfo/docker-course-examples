#!/usr/bin/env bash 

trap 'exit 0' SIGINT
trap 'exit 0' SIGTERM


get_random_message() {
    local arr=("$@")
    local random_index=$((RANDOM % ${#arr[@]}))
    echo "${arr[$random_index]}"
}


levels=(
    "error"
    "warning"
    "info"
    "debug"
)
error_messages=(
    "Произошла ошибка при запуске сервиса."
    "Произошла критическая ошибка в сервисе."
    "Сервис временно недоступен."
)
warning_messages=(
    "Сервис перезапускается..."
    "Сервис ожидает подключения."
    "Сервис обновляется, подождите..."
)
info_messages=(
    "Сервис успешно запущен."
    "Сервис остановлен."
    "Сервис работает в штатном режиме."
    "Сервис завершил свою работу."
)
debug_messages=(
    "Начало инициализации компонентов."
    "Подключение к базе данных установлено."
    "Отправка данных в лог."
)

echo ""
echo "* Logging imitator started"
echo "* CTRL+C to stop"
echo ""

while true; do
    now="$(date +"%Y-%m-%d %H:%M:%S")"
    level_no=$(($RANDOM % ${#levels[@]}))
    level=${levels[$level_no]}

    case $level in
        error)
            msg=$(get_random_message "${error_messages[@]}") ;;
        warning)
            msg=$(get_random_message "${warning_messages[@]}") ;;
        info)
            msg=$(get_random_message "${info_messages[@]}") ;;
        debug)
            msg=$(get_random_message "${debug_messages[@]}") ;;
    esac
    
    case $level in
        error|warning)
            echo >&2 "$now [$level] $msg" ;;
        info|debug)
            echo "$now [$level] $msg" ;;
    esac

    sleep $(($RANDOM % 5))
done
