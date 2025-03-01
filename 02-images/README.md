# Урок 2. Образы

- [Кратко об OverlasFS](#кратко-об-overlasfs)
- [Сборка образа example-layers](#сборка-образа-example-layers)
- [Изученные команды](#изученные-команды)
- [Вопросы](#вопросы)
- [Ссылки](#ссылки)

**Docker образ** - это шаблон, который содержит все необходимое для запуска приложения: код приложения, среду выполнения, библиотеки, зависимости и другие настройки.

## Кратко об OverlasFS

**Overlay Filesystem (OverlayFS)** - это механизм в ядре Linux, который позволяет объединять несколько файловых систем в одну виртуальную файловую систему. Он позволяет монтировать несколько файловых систем поверх друг друга таким образом, что файлы и каталоги из верхних слоев маскируют файлы и каталоги из нижних слоев. Каждый слой может быть только для чтения или для чтения и записи, и изменения могут быть сохранены только в верхнем слое, что делает его эффективным и удобным для развертывания и управления контейнерами.

OverlayFS объединяет две файловые системы - `upper` и `lower` или верхнюю и нижнюю. В контексте Docker используется термин **слои**. Когда имя существует в обоих слоях, объект в верхнем слое виден, в то время как объект в нижнем слое либо скрыт, либо, в случае каталогов, объединен с объектом из верхнего слоя.

Когда каталог в верхнем слое файловой системы создается с таким же именем, как и каталог в нижнем слое, и нижний каталог не пустой, то OverlayFS создает "непрозрачный каталог" (`opaque directory`). Содержимое каталогов объединяется таким образом, что при доступе через верхний слой мы видим содержимое верхнего и нижнего каталогов. Это позволяет избежать конфликтов и перекрытий между каталогами из разных слоев, сохраняя при этом доступ к содержимому обоих слоев.

Когда файл или каталог в верхнем слое файловой системы удаляется, но существует в нижних слоях, OverlayFS создает "белое пятно" (`whiteout`) в верхнем слое. Это специальный файл или каталог, который сообщает OverlayFS, что соответствующий файл или каталог должен быть скрыт, как будто бы его не существует. Это позволяет правильно обрабатывать удаление файлов и каталогов из верхнего слоя без изменения нижних слоев.

## Сборка образа example-layers

```bash
docker build -t example-layers ./example-layers
```

## Изученные команды

```bash
# Команды для управления образами Docker
docker image

# Список образов
docker image ls
# Короткий псевдоним
docker images

# Загрузка образов из реестра
docker pull debian
docker pull debian:bookworm-slim
docker pull debian:12-slim
docker pull kyzimaspb/flask:3.11-slim-bookworm

# Просмотр информации об образе
docker inspect debian:12-slim | less

# Просмотр истории создания образа Docker
docker pull nginx
docker history nginx

# Драйвер хранилища
docker info | grep -i storage
docker inspect nginx | less

# Просмотр истории образа example-layers без обрезки вывода
docker history --no-trunc example-layers

# Удаление образов
docker rmi debian:12-slim
docker rmi debian:bookworm-slim

# Удалить неиспользуемые образы
docker image prune
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



## Ссылки

* [Реестр Docker](https://hub.docker.com/)
* [Dive - Инструмент для изучения каждого слоя в образе Docker](https://github.com/wagoodman/dive)
* [Use the OverlayFS storage driver](https://docs.docker.com/storage/storagedriver/overlayfs-driver/)
* [Overlay Filesystem](https://www.kernel.org/doc/html/latest/filesystems/overlayfs.html)
