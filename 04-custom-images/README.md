# Урок 4. Пользовательские образы

- [Синтаксис Dockerfile](#синтаксис-dockerfile)
- [Пример запуска Django приложения в Docker контейнере](#пример-запуска-django-приложения-в-docker-контейнере)
  - [Инициализация проекта на Django](#инициализация-проекта-на-django)
  - [Команды для работы с образом](#команды-для-работы-с-образом)
- [Сборка мультиплатформенных образов](#сборка-мультиплатформенных-образов)
- [Экспорт и импорт образов](#экспорт-и-импорт-образов)
  - [Экспорт для архитектуры, отличной от хостовой](#экспорт-для-архитектуры-отличной-от-хостовой)
  - [Импорт мультиплатформенных образов в формате OCI](#импорт-мультиплатформенных-образов-в-формате-oci)
- [Ссылки](#ссылки)

## Синтаксис Dockerfile

> **Примечание**
>
> Начиная с версии [20.10](https://docs.docker.com/engine/release-notes/20.10/#deprecation--removal)
> синтаксис объявления переменной окружения `ENV name value` считается устаревшим.
> Упоминание об этом встречается в списке устаревших и удаленных возможностей к версии
> [26.1.4](https://github.com/docker/cli/blob/v26.1.4/docs/deprecated.md#dockerfile-legacy-env-name-value-syntax)
>
> Начиная с версии `27+` в консоль выводится предупреждение
> `LegacyKeyValueFormat: "ENV key=value" should be used instead of legacy "ENV key value" format`

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

3.  Устанавливает переменные среды
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

2.  Устанавливает одну переменную среды
    ENV <key> <value>
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

## Сборка мультиплатформенных образов

Сборщик по умолчанию не поддерживает некоторые расширенные функции buildx,
включая мультиплатформенные сборки и экспорт в формате [OCI](https://opencontainers.org/).

```bash
# Просмотр доступных сборщиков
# * отмечен текущий сборщик
docker buildx ls

# Просмотр информации о текущем сборщике
# -D выводит дополнительную информацию о сборщике
docker buildx inspect -D

# Создать новый сборщик с именем multi-oci и сделать текущим
docker buildx create --name multi-oci --use
# Тоже самое, но двумя командами
docker buildx create --name multi-oci
# Устанавливает сборщик с указанным именем как текущий
docker buildx use multi-oci

# Сборка мультиплатформенного образа для x86_64 и armv7 с загрузкой в реест
docker buildx build \
    --platform linux/amd64,linux/arm/v7 \
    -t kyzimaspb/example-multi-arch \
    --push \
        ./example-multi-arch

# Можно явно указать используемый сборщик
docker buildx build \
    --builder multi-oci \
    --platform linux/amd64,linux/arm/v7 \
    -t kyzimaspb/example-multi-arch \
    --push \
        ./example-multi-arch

# Просмотр доступных платформ для указанного образа
# (экспериментальная возможность)
docker manifest inspect kyzimaspb/example-multi-arch
```

## Экспорт и импорт образов

Когда у вас нет прямого доступа к реестру,
например это частный реестр внутри локальной сети компании,
либо целевая машина не подключена к сети,
возникает вопрос: "Как перенести образ на такую машину?"

В этом случае можно экспортировать образ в tar архив:

```bash
# Сборка образа с демо программой получения погоды в указанном городе
docker build \
    -t kyzimaspb/weather \
    -f ./example-weather/Dockerfile \
        ./example-weather/app

# Экспортируем образ в tar архив
docker save -o weather.tar kyzimaspb/weather
# Или со сжатием
docker save kyzimaspb/weather | gzip - > weather.tar.gz
```

А затем импортировать его на целевой машине:

```bash
docker load -i weather.tar.gz
```

Для запуска контейнера вам нужен токен доступа к одному из сервисов:
[OpenWeather][open-weather-map] или [WeatherAPI][weather-api]:

```bash
docker run --rm -ti \
    -e WEATHER_PROVIDER_NAME=open_weather_map \
    -e WEATHER_OPEN_WEATHER_MAP__API_KEY=0123456789 \
        kyzimaspb/weather Пермь
```

### Экспорт для архитектуры, отличной от хостовой

Создаем новый сборщик с именем `multi-oci` с поддержкой мультиплатформенности и делаем его текущим:

```bash
docker buildx create --name multi-oci --use
```

Buildx позволяет выполнять сборку образов для платформ, отличных от хостовой.
Собранный образ для **одной** платформы можно автоматически загрузить в `docker images`.
Однако, запустить контейнер на базе такого образа не получится из-за различия в архитектуре:

```bash
# Сборка образа для armv7 на x86
docker buildx build \
    --platform linux/arm/v7 \
    -t kyzimaspb/example-armv7 \
    --load \
        ./example-multi-arch

# WARNING: The requested image's platform (linux/arm/v7)
# does not match the detected host platform (linux/amd64/v2)
# and no specific platform was requested
# exec /usr/bin/arch: exec format error
docker run --rm kyzimaspb/example-armv7
```

Если ваша цель собрать образ для платформы, отличной от хостовой, и сохранить его на физическом носителе
без использования реестра или при отсутствии подключения к сети,
то вы можете собрать образ с экспортом в tar архив:

```bash
docker buildx build \                  
    --platform linux/arm/v7 \
    -t kyzimaspb/example-armv7 \
    --output type=docker,dest=armv7-image.tar \
        ./example-multi-arch
```

А затем импортировать его на целевой машине:

```bash
docker load -i armv7-image.tar
```

### Импорт мультиплатформенных образов в формате OCI

Лучше экспортировать образ для конкретной архитектуры, чем создавать мультиплатформенный.
Однако, если по каким-то причинам вам это нужно, то у меня получилось это сделать так:

* `ctr` - утилита для управления контейнерами в Containerd
* `-n moby` - пространства имён moby (Docker использует его для взаимодействия с Containerd)

```bash
# Сборка мультиплатформенного образа для x86_64 и armv7 с сохранением в tar архив
# Образ создан в формате OCI (с поддержкой нескольких платформ)
docker buildx build \
    --platform linux/amd64,linux/arm/v7 \
    -t kyzimaspb/example-multi-arch \
    --output type=oci,dest=multi-arch-image.tar \
        ./example-multi-arch

# Импорт мультиплатформенного образа в Containerd
ctr -n moby images import multi-arch-image.tar

# Экспорт в архив с явным указанием платформы (по-умолчанию платформа хоста) 
ctr -n moby images export \
    --platform linux/arm/v7 \
    armv7-image.tar \
    docker.io/kyzimaspb/example-multi-arch:latest

# Импорт в `docker images`
docker load -i armv7-image.tar

# Например, напечатает armv7l на OrangePI
docker run --rm kyzimaspb/example-multi-arch 
```

## Ссылки

* [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
* [Настройка приложения Django из переменных среды](https://django-environ.readthedocs.io/en/latest/)
* [Gunicorn - WSGI HTTP сервер](https://gunicorn.org/)

[https://openweathermap.org]: #open-weather-map
[https://www.weatherapi.com]: #weather-api
