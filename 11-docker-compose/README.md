# Урок 11. Docker Compose

* [Основные команды](#основные-команды)
* [Проект Uploader](#проект-uploader)
* [Подведение итогов](#подведение-итогов)
  * [Что делать, если Nginx нужен в обеих средах?](#что-делать-если-nginx-нужен-в-обеих-средах)
  * [Можно ли использовать этот шаблон для других стеков?](#можно-ли-использовать-этот-шаблон-для-других-стеков)
  * [Не рассмотренный синтаксис](#не-рассмотренный-синтаксис)
* [Ссылки](#ссылки)

В Docker считается хорошей практикой в одном контейнере запускать только одну службу:

* **изоляция** - каждый контейнер обеспечивает своё пространство имен, файловую систему и сеть,
  а значит не будет конфликтов с другими службами
* **масштабируемость** - можно масштабировать только те части вашего приложения,
  которые действительно нуждаются в увеличении производительности или доступности
* **управление** - проще мониторить, перезапускать или обновлять запущенную службу
* **упрощение сборки и тестирования** - каждая служба может иметь свои собственные зависимости и настройки,
  что уменьшает риск конфликтов и ошибок при разработке и тестировании
* **[принцип единственной ответственности](https://ru.wikipedia.org/wiki/Принцип_единственной_ответственности)** -
  каждый контейнер должен решать только одну задачу

Docker может автоматически следить за состоянием запущенной службы с идентификатором процесса 1.
Этот процесс также называется **init** процессом контейнера.

Если в контейнере запускается несколько процессов без явного определения PID 1,
Docker может столкнуться с проблемами при попытке управления контейнером,
например, при попытке перезапуска или остановки контейнера.

Если все таки необходимо запустить несколько служб в одном Docker контейнере, 
то стоит использовать инструменты для управления несколькими процессами,
например, [s6-overlay](https://github.com/just-containers/s6-overlay),
который может обеспечить корректное управление жизненным циклом процессов внутри Docker контейнера.

Docker Compose позволяет определять многоконтейнерные приложения и управлять ими в одном **файле YAML**.
Этот файл должен быть создан в корневой директории проекта:

* `compose.yaml` или `compose.yml` - имя по умолчанию
* `compose.override.yaml` или `compose.override.yml` - файл переопределения по умолчанию
* `docker-compose.yaml` или `docker-compose.yml` - имя по умолчанию для обратной совместимости 
* `docker-compose.override.yaml` или `docker-compose.override.yml` - файл переопределения по умолчанию для обратной совместимости

## Основные команды

> **Примечание**
>
> В некоторых источниках вы можете увидеть команду `docker-compose`, вместо `docker compose`. Это артефакт из прошлого.
> 
> Docker Compose V1 был написан на Python и распространялся как отдельный скрипт.
> Его скачивали (или устанавливали из официальных репозиториев дистрибутива Linux) к себе на ПК.
> Для этого скрипта закрепилось имя по умолчанию как `docker-compose`.
> На сегодня Docker Compose V1 считается устаревшим и не используется.
> 
> Docker Compose V2 был полностью переписан на Go в виде плагина.
> Поэтому после установки этого плагина, он доступен как подкоманда `compose` для команды `docker`.
> 
> Docker Compose V2 автоматически устанавливается вместе с Docker Desktop.
> В дистрибутивах Linux - если используется скрипт автоматической установки, иначе вручную.

Ниже я привожу список наиболее часто используемых Docker Compose команд:

```shell
# Просмотр запущенных Docker Compose проектов
docker compose ls [OPTIONS]

# Загрузка образов для сервисов, не требующих сборки
docker compose pull [OPTIONS] [SERVICE...]

# Сборка/пересборка всех или перечисленных служб
docker compose build [OPTIONS] [SERVICE...]

# Список образов, используемых созданными контейнерами
docker compose images [OPTIONS] [SERVICE...]

# Создать и запустить контейнеры для всех или перечисленных служб
docker compose up [OPTIONS] [SERVICE...]

# Выполнить команду для службы и выйти
docker compose run [OPTIONS] SERVICE [COMMAND] [ARGS...]

# Список запущенных контейнеров
docker compose ps [OPTIONS] [SERVICE...]

# Остановить запущенные сервисы - все или перечисленные
docker compose stop [OPTIONS] [SERVICE...]

# Остановить запущенные сервисы, затем удалить контейнеры и сети
docker compose down [OPTIONS] [SERVICES]

# Создать контейнеры для всех или перечисленных служб
docker compose create [OPTIONS] [SERVICE...]

# Запустить существующие контейнеры для всех или перечисленных служб
docker compose start [SERVICE...]

# Перезапустить контейнеры для всех или перечисленных служб
docker compose restart [OPTIONS] [SERVICE...]

# Выполнить команду в запущенном контейнере
docker compose exec [OPTIONS] SERVICE COMMAND [ARGS...]

# Скопировать файл из контейнера на хост
docker compose cp [OPTIONS] SERVICE:SRC_PATH DEST_PATH|-
# Скопировать файл с хоста в контейнер
docker compose cp [OPTIONS] SRC_PATH|- SERVICE:DEST_PATH

# Просмотр процессов в запущенных контейнерах
docker compose top [SERVICES...]

# Просмотр потребляемых контейнерами ресурсов
docker compose stats [OPTIONS] [SERVICE]

# Просмотр журналов контейнеров для всех или перечисленных служб
docker compose logs [OPTIONS] [SERVICE...]

# Удаляет остановленные контейнеры для всех или перечисленных служб
docker compose rm [OPTIONS] [SERVICE...]
```

## Проект Uploader

```shell
# Сборка проекта для среды разработки
docker compose build

# Запуск проекта в среде разработки в интерактивном режиме
docker compose up
# Запуск проекта в среде разработки в фоновом режиме
docker compose up -d
# Сборка и запуск проекта в среде разработки в фоновом режиме
docker compose up --build -d

# Сборка проекта для производственной среды
docker compose -f compose.yml build

# Запуск проекта в производственной среде
docker compose -f compose.yml up -d

# Просмотр конечной конфигурации, которую будет использовать Docker Compose
docker compose config

# Запуск проекта в среде разработки с профилем debug
docker compose --profile debug up -d
```

## Подведение итогов

### Что делать, если Nginx нужен в обеих средах?

В приведенном примере Nginx отсутствует в среде разработки.
Если по каким-то причинам он вам нужен в обеих средах,
то вместо Nginx можно отдавать статику простым сервером для статических файлов,
например, [lighttpd](https://www.lighttpd.net/).
Вам нужно заменить этап `production` в `Dockerfile` для сервиса `frontend`
и добавить новый сервис `nginx` в `compose.yml`.
Отредактировать конфигурационный файл виртуального хоста
и для запросов к корневому URL добавить проксирование к lighttpd.

Но в этом нет смысла, по двум причинам:

1. Если вы разрабатываете не закрытую систему, то обычно любой сайт должен проиндексировать поисковый робот.
   SPA на React/Vue.js - это JavaScript, который поисковый робот не умеет интерпретировать,
   все что он увидит - пустая страница. Поэтому нужно настроить SSR - отрисовку страницы на стороне сервера.
   
   Популярные frontend фреймворки предлагают готовые решения:
   
   * для [React](https://react.dev/) - это [Next.js](https://nextjs.org/)
   * для [Vue.js](https://vuejs.org/) - это [Nuxt](https://nuxt.com/)
   
   Эти фреймворки упрощают разработку приложений,
   предоставляя из коробки SSR, роутер и другие часто используемые дополнения.
   Встроенный сервер можно и нужно использовать для разработки и для производства,
   он заменяет Nginx на шаге `production`.
   Сервис `frontend` нужно оключить от сети `public` и убрать проброс портов. 
   Теперь все запросы к этому сервису будет проксировать Nginx,
   который нужно добавить в `compose.yml`:
   
   ```yaml
   services:
     nginx:
       image: nginx:1.27-bookworm
       networks:
         - private
         - public
       ports:
         - "80:80"
       configs:
         - source: nginx_default
           target: /etc/nginx/conf.d/default.conf
       volumes:
         - uploaderdata:/upload
       depends_on:
         - backend
         - frontend
       restart: unless-stopped
   ```
1. В большинстве случаев, разработка серверной части (если это API) и клиентской (если это SPA) ведется раздельно.

### Можно ли использовать этот шаблон для других стеков?

Короткий ответ: да, можно.

Мой шаблон можно адаптировать под любой стек веб разработчика.
Выбирайте любимый frontend фреймворк или будьте адептом старой школы.
Выбирайте любымый серверный фреймворк для вашего языка программирования,
а если вы любите пыхнуть, то можно и без них =)

Для питонистов это может быть:

* Более корпоративный стек - [Django](https://www.djangoproject.com/)
  и [Next.js](https://nextjs.org/) ([React](https://react.dev/)).
* Стек для энтузиастов - [Flask](https://flask.palletsprojects.com/en/3.0.x/)
  и [Nuxt](https://nuxt.com/) ([Vue.js](https://vuejs.org/))
* Для любителей асинхронности - [FastAPI](https://fastapi.tiangolo.com/)
  и [Next.js](https://nextjs.org/) ([React](https://react.dev/))

**Моя цель** - дать отправную точку для новичков в Docker, которой мне не хватало в 2017 году.
Показать как не дублировать Dockerfile файлы и не разводить зоопарк yml файлов.

**Ваша цель** - доработать или разработать свой шаблон.

### Не рассмотренный синтаксис

Большинство параметров, которые можно указать при описании сервисов, сетей, томов и т.п.,
совпадают полностью или почти с именами аргументов для команд Docker CLI.

Если аргумент имеет логическое значение, то в `compose.yml` нужно использовать `true` или `false`.
Если аргумент можно передавать многократно, то в `compose.yml` нужно использовать список с именем во множественном числе,
например `--network` и `networks`.
Поэтому я не думаю, что у вас могут возникнуть проблемы.

Продвинутый синтаксис, позволяющий включать `yml` файлы, расширять списки и словари, переопределять или затирать значения,
новые возможности, например, [Watch](https://docs.docker.com/compose/file-watch/),
я не стал рассматривать по нескольким причинам:

* ограниченное время занятия
* на момент записи некоторые возможности были доступны только в последней версии Docker Compose
* пока еще кажется "сырым"
* начинающим работать с Docker Compose будет достаточно знаний из урока для старта 

## Ссылки

* [Docker docs - Docker Compose overview](https://docs.docker.com/compose/)
* [s6 overlay for containers](https://github.com/just-containers/s6-overlay)
* [Adminer - Database management in a single PHP file](https://www.adminer.org/)
* [Web-based MongoDB admin interface](https://github.com/mongo-express/mongo-express)
* [Scaffolding Your First Vite Project](https://vitejs.dev/guide/#scaffolding-your-first-vite-project)
* [Configuring Vite - server.proxy](https://vitejs.dev/config/server-options.html#server-proxy)
