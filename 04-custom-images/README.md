# Урок 4. Пользовательские образы

## Синтаксис Dockerfile

```
Создают новый слой

1.  Задает базовый образ, на основе которого будет создаваться текущий образ
    FROM [--platform=<platform>] <image> [AS <name>]
    FROM [--platform=<platform>] <image>[:<tag>] [AS <name>]
    FROM [--platform=<platform>] <image>[@<digest>] [AS <name>]

2.  Выполняет команды на этапе сборки
    RUN [OPTIONS] <command> ...
    RUN [OPTIONS] [ "<command>", ... ]

3.  Копирует файлы и каталоги
    COPY [OPTIONS] <src> ... <dest>
    COPY [OPTIONS] ["<src>", ... "<dest>"]

4.  Добавляет локальные или удаленные файлы и каталоги
    ADD [OPTIONS] <src> ... <dest>
    ADD [OPTIONS] ["<src>", ... "<dest>"]

Изменяют метаинформацию образа
(во время сборки создают временные промежуточные слои)

1.  Задает команду, выполняемую при старте контейнера или аргументы ENTRYPOINT
    CMD ["executable","param1","param2"]
    CMD ["param1","param2"]
    CMD command param1 param2

2.  Задает исполняемый файл, который будет выполнен всегда при старте контейнера
    ENTRYPOINT ["executable", "param1", "param2"]
    ENTRYPOINT command param1 param2

3.  Установливает переменную(ые) среды
    ENV <key> <value>
    ENV <key>=<value> ...

4.  Описывает, какие порты прослушивает ваше приложение
    EXPOSE <port> [<port>/<protocol>...]

5.  Задает команду проверки состояния (работоспособности) контейнера
    HEALTHCHECK [OPTIONS] CMD command
    HEALTHCHECK NONE

6.  Добавляет метаданные к образу
    LABEL <key>=<value> <key>=<value> <key>=<value> ...

7.  Устанавливает оболочку образа по умолчанию
    SHELL ["executable", "parameters"]

8.  Задает сигнал системного вызова для выхода из контейнера
    STOPSIGNAL signal

9.  Задает идентификатор пользователя и группы
    USER <user>[:<group>]
    USER UID[:GID]

10. Создает точку монтирования тома
    VOLUME /data ...
    VOLUME ["/data"]

11. Задает текущий рабочий каталог
    WORKDIR /path/to/workdir

Используемые во время сборки

1.  Устанавливает переменную времени сборки
    ARG <name>[=<default value>]

2.  Добавляет команду запуска, которая будет выполняться позже,
    когда образ будет использоваться в качестве основы для другой сборки
    ONBUILD INSTRUCTION

Устаревшие

1.  Указывает автора образа
    MAINTAINER <name>
    LABEL maintainer="Kirill Vercetti <office@kyzima-spb.com>"
```


## Пример запуска Django приложения в Docker контейнере

### Инициализация проекта на Django

Команда инициализирует пустой проект в текущей директории.
Но требуется небольшая модификация файла настроек,
для поддержки всех возможностей из примера:

```shell
docker run --rm -ti \
    -u $(id -u):$(id -g) \
    -e HOME=/tmp \
    -v $(pwd):/app \
    -w /app \
    python:3.12-slim-bookworm \
        bash -c '
            set -ex;
            pip install Django django-environ gunicorn;
            /tmp/.local/bin/django-admin startproject mysite .;
            pip freeze | grep -vE "^(setuptools|wheel)" > requirements.txt;
        '
```

### Команды для работы с образом

```shell
# Сборка образа
docker build -t example-django .

# Сборка образа в переходных версиях Docker
DOCKER_BUILDKIT=1 docker build -t example-django .

# Добавление новой метки к образу
docker tag example-django example-django:1.0.0

# Запуск контейнера с Django в производственной среде
docker run --rm -ti --name django_1 -p 8000:8000 example-django

# Запуск контейнера с Django в среде разработки
# -v $(pwd):/app в уроке не было, но оставлено для чистоты примера
docker run --rm -ti --name django_1 \
    -p 8000:8000 \
    -e DEBUG=1 \
    -v $(pwd):/app \
    example-django \
        python manage.py runserver 0.0.0.0:8000

# Аутентификация в реестре Docker
docker login -u <USERNAME>

# Добавление новой метки перед публикацией в реестре Docker
docker tag example-django <USERNAME>/example-django

# Сборка образа для публикации в реестре Docker
docker build -t <USERNAME>/example-django:1.0.0 .

# Публикация образа в реестре Docker
docker push <USERNAME>/example-django
docker push <USERNAME>/example-django:1.0.0

# Очистка системы от:
# - остановленных контейнеров
# - не используемых хотя бы одним контейнером сетей
# - не связанных ни с одним контейнером образов
# - всего кеша сборки
docker system prune -a
```

## Ссылки

* [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
* [Настройка приложения Django из переменных среды](https://django-environ.readthedocs.io/en/latest/)
* [Gunicorn - WSGI HTTP сервер](https://gunicorn.org/)
