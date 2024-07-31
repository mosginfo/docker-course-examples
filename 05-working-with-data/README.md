# Урок 5. Управление данными в Docker, пользователи

- [Bind mounts – на примере веб приложения Uploader](#bind-mounts--на-примере-веб-приложения-uploader)
- [Volumes](#volumes)
  - [Чем volume лучше bind mount?](#чем-volume-лучше-bind-mount)
  - [Создание томов вручную](#создание-томов-вручную)
  - [Анонимные тома](#анонимные-тома)
- [tmpfs](#tmpfs)
- [Удаление томов](#удаление-томов)
- [Вопросы](#вопросы)
- [Ссылки](#ссылки)

## Bind mounts – на примере веб приложения Uploader

Не возможно редактировать исходные файлы приложения без пересборки.
На помощь приходят тома и тип монтирования bind mounts.

**Bind mounts** - это способ монтирования каталогов или файлов с хоста в контейнеры. Этот метод монтирования позволяет контейнеру получать доступ к данным, находящимся на хосте, таким образом, что любые изменения, сделанные внутри контейнера, сразу же видны на хосте, и наоборот.

Bind mounts используются для различных целей, включая совместное использование данных между контейнерами и хостом, а также для разработки и тестирования приложений.

```shell
# Сборка образа
docker build -t example-uploader -f Dockerfile ./uploader

# Запускаем сервер разработки Flask и монтируем исходный код приложения.
docker run --rm -ti \
    --name uploader_1 \
    -p "127.0.0.1:5000:5000" \
    -v "$(pwd)/uploader:/app" \
    -e FLASK_DEBUG=1 \
    -e FLASK_UPLOADER_ROOT_DIR=/app/upload \
        example-uploader \
            flask run -h 0.0.0.0

# Просмотр загруженных файлов
docker exec uploader_1 ls -laR upload
# Удаление всех загруженных файлов
docker exec uploader_1 rm -rf upload/*

# Изменяем имя пользователя и группу
docker run --rm -ti \
    --name uploader_1 \
    -u $(id -u):$(id -g) \
    -p "127.0.0.1:5000:5000" \
    -v "$(pwd)/uploader:/app" \
    -e FLASK_DEBUG=1 \
    -e FLASK_UPLOADER_ROOT_DIR=/app/upload \
        example-uploader \
            flask run -h 0.0.0.0

# Запуск приложения от пользователя не из Dockerfile
docker run --rm -ti \
    --name uploader_1 \
    -u www-data:www-data \
    -p "127.0.0.1:5000:5000" \
    -v "$(pwd)/uploader:/app" \
    -e FLASK_DEBUG=1 \
        example-uploader \
            flask run -h 0.0.0.0
```

## Volumes

С помощью инструкции `VOLUME` можно описать точки монтирования томов.

Тома в Docker нужны для обеспечения сохранности данных, например, файлов - загруженных пользователем, или файлов СУБД и тому подобных.

Любой, кто будет просматривать информацию об образе, узнает, какие пути в контейнере используются для сохранения постоянных данных.

Docker будет создавать том даже если не указан аргумент `-v` или `--mount`.

### Чем volume лучше bind mount?

1. Легче выполнять резервное копирование или миграцию.
2. Драйверы томов позволяют использовать разные хранилища,
   например, NFS, Samba, SSHFS, облако, или шифровать данные.
3. Можно предварительно инициализировать топ нужными данными в `Dockerfile`.

```shell
# Пример с загруженными пользователем файлами
docker run --rm -ti \
    --name uploader_1 \
    -p "127.0.0.1:5000:5000" \
    -v uploader_data:/upload \
        example-uploader

# Пример с СУБД PostgeSQL

# Просмотр задекларированных томов в образе
docker pull postgres:16.2-bookworm
docker inspect --format '{{json .Config.Volumes}}' postgres:16.2-bookworm

# Стартуем контейнер с использованием именованного тома
docker run --rm -d \
    --name postgres_1 \
    -e POSTGRES_PASSWORD=toor \
    -e POSTGRES_DB=demo \
    -v pgdata:/var/lib/postgresql/data \
        postgres:16.2-bookworm

# Вручную применяем схему для БД
docker exec -i postgres_1 psql -U postgres demo < schema.pg.sql

# Выбираем из БД все категории
docker exec -i postgres_1 psql -U postgres demo -c 'SELECT * FROM category;'
```

### Создание томов вручную

```shell
# Просмотр доступных драйверов для создания томов
docker info --format '{{.Plugins.Volume}}'

# Создает NFS том
docker volume create \
    -d local \
    -o type=nfs \
    -o o=addr=192.168.88.184,nfsvers=4 \
    -o device=:/docker_volumes/dbdata/mongo_example \
        mongodata_nfs

# Просмотр информации о томах
docker inspect mongodata_nfs

# Просмотр задекларированных томов в образе
docker pull mongo:7.0.11-jammy
docker inspect --format '{{json .Config.Volumes}}' mongo:7.0.11-jammy

# Стартуем контейнер с указанием NFS-тома
docker run --rm -d \
    --name mongo_1 \
    -e MONGO_INITDB_ROOT_USERNAME=mongoadmin \
    -e MONGO_INITDB_ROOT_PASSWORD=secret \
    -v mongodata_nfs:/data/db \
        mongo:7.0.11-jammy

# Вручную добавляем данные в коллекцию categories
docker exec -i mongo_1 mongosh -u mongoadmin -p secret < categories.js

# Выбираем все элементы коллекции categories
docker exec mongo_1 mongosh -u mongoadmin -p secret --eval 'db.categories.find()'
```

### Анонимные тома

**Анонимный том** - это том, который Docker создает автоматически и управляет его жизненным циклом.

Когда вы указываете только один путь после флага `-v`, Docker создает анонимный том.
Он не привязан к конкретному пути на хосте и его путь выглядит как случайно сгенерированный идентификатор.

Анонимные тома полезны в в том случае, если:

* вам нужно временное хранилище, которое не требует сохранения после удаления контейнера
* вам нужно изолировать данные контейнера от хостовой файловой системы

## tmpfs

**Tmpfs** (temporary file system) - это файловая система, которая хранит все свои файлы в виртуальной памяти.

Все в `tmpfs` является временным в том смысле, что на вашем жестком диске не будут созданы файлы. Если вы размонтируете экземпляр `tmpfs`, все, что в нем хранится, будет потеряно.

Это может быть полезно для хранения временных данных, которые не нужно сохранять между перезапусками контейнеров Docker.


```shell
# Стартуем контейнер с PostgreSQL, которая хранит свои данные в tmpfs
docker run --rm -d \
    --name postgres_1 \
    -e POSTGRES_PASSWORD=toor \
    -e POSTGRES_DB=demo \
    --mount type=tmpfs,destination=/var/lib/postgresql/data \
        postgres:16.2-bookworm

# Короткая версия аргумента --mount это --tmpfs
docker run --rm -d \
    --name postgres_2 \
    -e POSTGRES_PASSWORD=toor \
    -e POSTGRES_DB=demo \
    --tmpfs /var/lib/postgresql/data \
        postgres:16.2-bookworm

# Просмотр смонтированных файловых систем как tmpfs в запущенном контейнере
docker exec postgres_1 mount | grep ^tmpfs

# Просмотр смонтированных файловых систем как tmpfs (не работает для аргумента --tmpfs)
docker inspect --format '{{json .Mounts}}' postgres_1
```

## Удаление томов

```shell
# Удалить выбранный том
docker volume rm <VOLUME_NAME>

# Удалить все не используемые анонимные тома
docker volume prune

# Удалить все не используемые тома
docker volume prune -a
```

## Вопросы

> Как докер понимает что в одном случае `-v source:target` это том, а в другом что это папка?

`-v test:/mount_point` - это имя тома, потому что нет явного указания пути,
а папка `test` в текущей директории должна быть указана как `-v ./test:/mount_point`.

`-v ./test:/mount_point`, `-v "$(pwd)/test:/mount_point"` или `-v /test:/mount_point` -
это монтирование директории с хостовой машины, потому что есть символ разделителя путей:

```
➜  docker volume create ./test
Error response from daemon: create ./test: "./test" includes invalid characters for a local volume name, only "[a-zA-Z0-9][a-zA-Z0-9_.-]" are allowed. If you intended to pass a host directory, use absolute path
```

## Ссылки

* [Docker docs - Volumes](https://docs.docker.com/storage/volumes/)
* [Tmpfs](https://www.kernel.org/doc/html/latest/filesystems/tmpfs.html)
* [Команда chown Linux](https://losst.pro/komanda-chown-linux)
* [Команда chmod Linux](https://losst.pro/komanda-chmod-linux)
* [Команда umask в Linux](https://losst.pro/komanda-umask-v-linux)
* [Настраиваем сетевую файловую систему NFS в Debian и Ubuntu](https://interface31.ru/tech_it/2023/07/
nastraivaem-setevuyu-faylovuyu-sistemu-nfs-v-debian-i-ubuntu.html)
* [Tmpfs](https://www.kernel.org/doc/html/latest/filesystems/tmpfs.html)
* [SSHFS](https://ru.wikipedia.org/wiki/SSHFS)
* [Расширение Flask-Uploader](https://flask-uploader.readthedocs.io/ru/latest/)
* [Simple Go-based setuid+setgid+setgroups+exec](https://github.com/tianon/gosu)
* [Alpine - Switch user and group id and exec](https://github.com/ncopa/su-exec)
