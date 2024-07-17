# Урок 10. Сети

- [Сетевые драйверы](#сетевые-драйверы)
- [bridge](#bridge)
  - [Сеть по умолчанию](#сеть-по-умолчанию)
  - [Пользовательские сети](#пользовательские-сети)
  - [Пользовательский мост VS мост по умолчанию](#пользовательский-мост-vs-мост-по-умолчанию)
  - [Подключение запущенного контейнера к сети](#подключение-запущенного-контейнера-к-сети)
  - [Отключение запущенного контейнера от сети](#отключение-запущенного-контейнера-от-сети)
  - [Cопоставление портов](#cопоставление-портов)
- [host](#host)
- [none](#none)
- [Внутренние сети](#внутренние-сети)
- [Ссылки](#ссылки)

## Сетевые драйверы

В Docker по умолчанию существует несколько драйверов, которые обеспечивают основные сетевые функции:

* **bridge** - сетевой драйвер по умолчанию,
  используется, когда запущенному в контейнере сервису,
  необходимо взаимодействовать с другими контейнерами на том же хосте
* **host** - использовать сеть хостовой машины напрямую
* **overlay** - соединяет несколько хостов-демонов Docker вместе
* **ipvlan** - позволяет контейнерам иметь свои IP-адреса в той же подсети, что и хостовая машина
* **macvlan** - позволяет контейнерам иметь собственные MAC-адреса
  и взаимодействовать в сети как отдельные физические устройства
* **none** - полная изоляция контейнера от хоста и других контейнеров

```shell
# Команды для управления сетями Docker
docker network

# Список доступных сетей
docker network ls
```

Чаще всего используются `bridge`, `host` и `none`.

## bridge

**[Сетевой мост](https://ru.wikipedia.org/wiki/Сетевой_мост)** -
это устройство канального уровня ([L2](https://ru.wikipedia.org/wiki/Канальный_уровень)) сетевой модели OSI.
Предназначен для объединения сегментов компьютерной сети в единую сеть.

Мостовая сеть в Docker использует программный мост,
который позволяет контейнерам, подключенным к той же мостовой сети,
обмениваться данными, обеспечивая при этом изоляцию от контейнеров,
которые не подключены к этой мостовой сети.

### Сеть по умолчанию

```shell
# Список сетевых интерфейсов хостовой машины
ip addr

# Запуск контейнера в сети bridge (в сети по умолчанию)
docker run --rm -tid --name nginx nginx:1.27-alpine3.19

# Получить IP-адрес контейнера в сети bridge
docker inspect nginx --format '{{json .NetworkSettings.Networks.bridge.IPAddress}}'

# Проверка доступности nginx по IP-адресу
ping <IP_ADDRESS>
# Запуск контейнера в сети bridge и проверка доступности nginx по IP-адресу
docker run --rm -ti alpine:3.19 ping <IP_ADDRESS>
# Запуск контейнера в сети bridge и проверка доступности nginx по идентификатору контейнера
docker run --rm -ti alpine:3.19 ping $(docker ps -q --filter name=nginx)
# Запуск контейнера в сети bridge и проверка доступности nginx по имени контейнера
docker run --rm -ti alpine:3.19 ping nginx

# Отображение списка сетевых интерфейсов
docker exec -ti nginx ip addr
```

### Пользовательские сети

```shell
# Создаем сеть с именем custom и драйвером bridge
docker network create -d bridge custom
# Создаем сеть с именем custom и драйвером по умолчанию bridge
docker network create custom

# Проверяем
docker network ls | grep custom
# Если по каким-то причинам вам не доступен grep
docker network ls -f name=custom

# Запуск контейнера в сети custom
docker run --rm -tid --name apache --network custom httpd:2.4-alpine3.19

# Получить IP-адрес контейнера в сети custom
docker inspect apache --format '{{json .NetworkSettings.Networks.custom.IPAddress}}'

# Проверка доступности apache по IP-адресу
ping <IP_ADDRESS>
# Запуск контейнера в сети bridge и проверка доступности apache
docker run --rm -ti alpine:3.19 ping <IP_ADDRESS>
# Запуск контейнера в сети custom и проверка доступности apache по IP-адресу
docker run --rm -ti --network custom alpine:3.19 ping <IP_ADDRESS>
# Запуск контейнера в сети custom и проверка доступности apache по идентификатору контейнера
docker run --rm -ti --network custom alpine:3.19 ping $(docker ps -q --filter name=apache)
# Запуск контейнера в сети custom и проверка доступности apache по имени контейнера
docker run --rm -ti --network custom alpine:3.19 ping apache
```

### Пользовательский мост VS мост по умолчанию

Мостовая сеть с именем `bridge`, используемая по умолчанию, не умеет:

1.  степень изоляции больше
1.  специфичные [настройки](https://docs.docker.com/network/drivers/bridge/#options) для каждого моста
1.  автоматическое разрешение DNS между контейнерами
    ```shell
    # вернет null
    docker inspect nginx --format '{{json .NetworkSettings.Networks.bridge.DNSNames}}'
    # вернет массив из двух элементов: идентификатор и именя контейнера
    docker inspect apache --format '{{json .NetworkSettings.Networks.custom.DNSNames}}'
    ```

### Подключение запущенного контейнера к сети

```shell
# Подключить контейнер с nginx к сети custom
docker network connect custom nginx

# Просмотр сетей, к которым подключен контейнер
docker inspect nginx --format '{{.NetworkSettings.Networks}}'
```

### Отключение запущенного контейнера от сети

```shell
# Отключить контейнер с nginx от сети по-умолчанию bridge
docker network disconnect bridge nginx

# Просмотр сетей, к которым подключен контейнер
docker inspect nginx --format '{{.NetworkSettings.Networks}}'
```

### Cопоставление портов

```shell
# Загрузка главной страницы из сети custom
docker run --rm -ti --network custom curlimages/curl nginx

# Загрузка главной страницы с хостовой машины
curl <IP_ADDRESS>
# завершится ошибкой
curl 127.0.0.1

# Проброс TCP портов 80 и 443 на хостовую машину
docker stop nginx
docker run --rm -tid --name nginx \
    --network custom \
    -p "127.0.0.1:80:80" \
    -p "127.0.0.1:443:443" \
    nginx:1.27-alpine3.19

# Просмотр открытых портов
# символ "->" означает сопоставление портов
docker port nginx

# Загрузка главной страницы с хостовой машины завершится успешно
curl 127.0.0.1
# Загрузка главной страницы из сети custom завершится успешно
docker run --rm -ti --network custom curlimages/curl nginx

# Запуск контейнера со службой точного времени
# NTP сервер использует UDP порт 123
docker run --rm -tid --name ntp \
    --network custom \
    -p "123:123/udp" \
    dockurr/chrony

# Открыты порты для ipv4 и ipv6
docker port ntp
```

## host

При использовании сети с именем `host` сетевой стек контейнера не изолирован от хостовой машины
и контейнеру не назначается собственный IP-адрес:

```shell
# Запуск контейнера в сети host
docker run --rm -tid --name apache --network host httpd:2.4-alpine3.19

# Проверяем, что IP адрес не был назначен
docker inspect apache --format '{{json .NetworkSettings.Networks.host.IPAddress}}'

# Проверяем, что все сетевые интерфейсы идентичны с хостовой машиной
ip -o -4 addr show | awk '{print $2, $4}'
docker exec apache ip -o -4 addr show | awk '{print $2, $4}'
```

Что нужно знать об этой сети:

* сопоставление портов не требуется, все открытые порты автоматически доступны с хостовой машины:
  ```shell
  curl 127.0.0.1
  ```
* используется для оптимизации производительности
  или если контейнеру необходимо обрабатывать большой диапазон портов,
  т.к. нет накладных расходов на преобразование сетевых адресов ([NAT](https://ru.wikipedia.org/wiki/NAT))

## none

Сеть с именем `none` используется, если нужна полная изоляция сетевого стека контейнера:

```shell
# Стартуем контейнер в сети none
docker run --rm -tid \
    --name example_none \
    --network none \
    --stop-signal SIGKILL \
    alpine:3.19

# Проверяем, что IP адрес не был назначен
docker inspect example_none --format '{{json .NetworkSettings.Networks.none.IPAddress}}'

# Проверяем, что существует только lo интерфейс
docker exec example_none ip addr

# Проверяем доступность удаленного ресурса
docker exec example_none ping google.com
```

## Внутренние сети

**Внутренняя сеть** - не будет иметь внешнего доступа, контейнеры внутри этой сети смогут общаться между собой,
но не смогут общаться с внешними ресурсами, такими как интернет или другие сети.

1. **Безопасность**: Внутренние сети изолируют контейнеры от внешнего мира, что снижает риски несанкционированного доступа.
   Это полезно для создания безопасных сред, например, для тестирования или разработки, где не нужен доступ к интернету.
1. **Контроль доступа**: Внутренние сети позволяют четко контролировать, какие контейнеры могут взаимодействовать друг с другом.
   Это позволяет структурировать архитектуру приложения и разделять различные части системы, ограничивая доступ только к необходимым ресурсам.
1. **Снижение количества исходящего трафика**: Когда контейнеры не имеют доступа к интернету,
   это помогает избежать случайного или неуместного исходящего трафика,
   что может быть полезно для контроля затрат на использование сетевых ресурсов и обеспечения приватности данных.

Аргумент `--internal` поддерживается сетевыми драйверами `bridge` и `overlay`.

```shell
# Создаем внутреннюю сеть с именем custom_internal и драйвером bridge
docker network create --internal custom_internal

# Запуск контейнеров в сети custom_internal
docker run --rm -tid \
    --name apache_internal \
    --network custom_internal \
    httpd:2.4-alpine3.19
docker run --rm -tid \
    --name nginx_internal \
    --network custom_internal \
    -p "80:80" \
    nginx:1.27-alpine3.19

# Проверяем доступность удаленного ресурса
docker exec apache_internal ping google.com
docker exec nginx_internal ping google.com

# Проверяем связь между контейнерами
docker exec apache_internal ping nginx_internal
docker exec nginx_internal ping apache_internal

# Проверяем доступность nginx с хостовой машины
curl 127.0.0.1

# Проверяем доступность nginx с хостовой машины по IP-адресу
docker inspect apache_internal --format '{{json .NetworkSettings.Networks.custom_internal.IPAddress}}'
curl <IP_ADDRESS>
```

## Ссылки

* [Docker docs - Networking overview](https://docs.docker.com/network/)
* [Network Time Protocol - протокол сетевого времени](https://ru.wikipedia.org/wiki/NTP)
* [Docker networking is CRAZY!! (you NEED to learn it)](https://www.youtube.com/watch?v=bKFMS5C4CG0)
