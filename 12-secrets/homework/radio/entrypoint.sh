#!/usr/bin/env sh

# Опция указывает завершать выполнение скрипта при первой же ошибке
# Поэтому выход с ненулевым кодом в вашем скрипте
# остановит выполнение и не даст запуститься серверу Icecast
set -e

# Здесь выполняем скрипт на вашем языке программирования


# Выполняем команду с аргументами, указанную в инструкции CMD
exec "$@"
