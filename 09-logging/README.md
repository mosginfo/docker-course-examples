# Урок 9. Журналирование

Запущенная в Docker-контейнере служба должна записывать свои логи в стандартный поток вывода и в стандартный поток ошибок.
В противном случае, команды для работы с журналами в Docker будут не доступны.

```shell
# Сборка демо образа со скриптом имитатора ведения журнала
docker build -t logging-imitator ./logging-imitator

# Запускаем контейнер с имитатором в режиме демона
docker run --rm -d --name imitator_1 logging-imitator

# Просмотр логов контейнера
docker logs imitator_1
```

## Фильтрация журнала

```shell
# В справочной информации есть все необходимые опции
docker logs --help

# Показать 10 последних записей из журнала
docker logs --tail 10 imitator_1

# Показать записи из журнала с указанного момента:
# - за последнюю минуту
docker logs --since 1m imitator_1
# - за последние 5 секунд
docker logs --since 5s imitator_1
# - исключая последние 5 минут
docker logs --until 5m imitator_1
# за последние 5 минут, но исключая последние 3 минуты
docker logs --since 5m --until 3m imitator_1
# - за указанный период
docker logs --since "<ISO_DATE>" --until "<ISO_DATE>" imitator_1

# Показать только STDOUT
docker logs imitator_1 2>/dev/null

# Показать только STDERR
docker logs imitator_1 > /dev/null

# Можно комбинировать с параметрами фильтрации
# Показать 15 последних записей журнала, исключая ошибки
docker logs --tail 15 imitator_1 2>/dev/null

# Показать записи из журнала с уровнем info
docker logs imitator_1 2>&1 | grep -F "info"
```

## Работа в режиме реального времени

```shell
# Просмотр журнала в режиме реального времени
docker logs -f imitator_1

# Просмотр журнала в режиме реального времени с фильтрацией
docker logs -f imitator_1 2>&1 | grep -F "debug"
```

## Драйверы ведения журнала

* **json-file** - драйвер ведения журнала по умолчанию, ротация отключена
* **local** - внутренний формат, использует сжатие и ротацию
* **none** - отключение ведения журнала

<hr>

* **journald** - использовать [journald](https://sysadmin.pm/journald-journalctl/) в системах с [systemd](https://ru.wikipedia.org/wiki/Systemd)
  (большинство современных дистрибутивов Linux)
* **syslog** - испльзовать [syslog](https://ru.wikipedia.org/wiki/Syslog) в системах с [sysvinit](https://ru.wikipedia.org/wiki/Init)
  (например, [Devuan](https://www.devuan.org/))

<hr>

* **gelf** - записывает сообщения журнала в конечную точку Graylog Extended Log Format (GELF),
  такую как [Graylog](https://www.graylog.org/) или [Logstash](https://www.elastic.co/products/logstash)
* **fluentd** - записывает сообщения журнала в [fluentd](https://www.fluentd.org/) (прямой ввод)
* **awslogs** - записывает сообщения журнала в журналы [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/details/#log-monitoring)
* **splunk** - записывает сообщения журнала в [splunk с помощью сборщика событий HTTP](https://dev.splunk.com/enterprise/docs/devtools/httpeventcollector/)
* **etwlogs** - записывает сообщения журнала в виде событий отслеживания событий Windows (ETW)
* **gcplogs** - записывает сообщения журнала в журнал [Google Cloud Platform](https://cloud.google.com/logging/docs/) (GCP)

```shell
# Текущий драйвер журнала
docker info --format '{{.LoggingDriver}}'

# Запуск контейнера с указанием драйвера ведения журнала
docker run --rm -d --name imitator_2 \
    --log-driver journald \
    logging-imitator

# Просмотр журнала для контейнера
# Нужны права суперпользователя или быть в группе adm или systemd-journal
sudo journalctl CONTAINER_NAME=imitator_2

# Просмотр журнала в режиме реального времени
sudo journalctl CONTAINER_NAME=imitator_2 -f

# Просмотр журнала в режиме реального времени с фильтрацией
sudo journalctl CONTAINER_NAME=imitator_2 -f | grep "warning"

# Запуск контейнера с указанием драйвера ведения журнала
# и дополнительными данными, которые нужно добавить в журнал
docker run --rm -d --name imitator_2 \
    --label version=3.12 \
    --label os=debian \
    --log-driver journald \
    --log-opt labels=version,os \
    logging-imitator

# Запуск контейнера с выключенным журналом
docker run --rm -d --name imitator_3 \
    --log-driver none \
    logging-imitator
```

## Настройка ведения журнала по умолчанию

| ОС                    | Путь к файлу конфигурации                   |
| --------------------- | ------------------------------------------- |
| Linux                 | `/etc/docker/daemon.json`                   |
| Linux (rootless mode) | `~/.config/docker/daemon.json`              |
| MacOS                 | `~/.docker/daemon.json`                     |
| Windows               | `C:\ProgramData\docker\config\daemon.json`  |
| Docker Desktop        | Preferences -> Docker engine                |

Можно настроить ротацию журнала для драйвера `json-file`, однако сжатие он не поддерживает.
Указываем параметры, которые используются по умолчанию для драйвера `local`:
максимальный размер файла `20Mb` и максимальное количество файлов `5`.
Таким образом размер журнала для каждого контейнера не будет превышать `100Mb`:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "20m",
    "max-file": "5"
  }
}
```

Для `systemd` выполняем перезапуск демона Docker.
Для других ОС просто перезапускаем Docker Desktop:

```shell
sudo systemctl daemon-reload && sudo systemctl restart docker

```

## Ссылки

* [Docker docs - Configure logging drivers](https://docs.docker.com/config/containers/logging/configure/)
* [ISO 8601 - международный стандарт, который описывает форматы дат и времени](https://en.wikipedia.org/wiki/ISO_8601)
* [Linux - Потоки, перенаправление потоков, конвейер](https://interface31.ru/tech_it/2021/10/linux---nachinayushhim-chast-7-potoki-perenapravlenie-potokov-konveyer.html)
* [man grep](https://www.man7.org/linux/man-pages/man1/grep.1.html)
* [GREP регулярные выражения. Поиск в Linux (кратко, но с юмором =)](https://www.youtube.com/watch?v=PBkJIRmWynM)
