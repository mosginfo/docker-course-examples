# Урок 7. Переменные времени сборки

## Пример. Webone HTTP 1.x Proxy

```bash
# Сборка образа Webone
docker build -t example-webone .

# Запуск контейнера с конфигурацией по-умолчанию
docker run --rm -ti \
       --name webone_1 \
       -p "8080:8080" \
       example-webone

docker build \
       -t example-webone:0.16.2 \
       --build-arg WEBONE_VERSION=0.16.2 \
       .

# Запуск контейнера с пользовательской конфигурацией
docker run --rm -ti \
       --name webone_1 \
       -p "8080:8080" \
       -v "$(pwd)/webone.conf:/opt/webone/webone.conf" \
       example-webone
```

## Ссылки

* [Docker docs - Build variables](https://docs.docker.com/build/building/variables/)
* [Webone HTTP 1.x Proxy](https://github.com/atauenis/webone)
* [Official images for .NET and ASP.NET Core](https://hub.docker.com/_/microsoft-dotnet/)
* [HTTP заголовок ETag](https://developer.mozilla.org/ru/docs/Web/HTTP/Headers/ETag)
* [HTTP заголовок Last-Modified](https://developer.mozilla.org/ru/docs/Web/HTTP/Headers/Last-Modified)
* [GNU Wget](https://www.gnu.org/software/wget/)
* [Команда wget Linux](https://losst.pro/komanda-wget-linux)
* [cURL](https://ru.wikipedia.org/wiki/CURL)
* [Как пользоваться curl](https://losst.pro/kak-polzovatsya-curl)
* [WebOne: Выходим в интернет в 2024 году через IE6 и Firefox 3](https://youtu.be/Rflb7_M7QSU)
* [WebOne: Выходим в интернет в 2024 году через IE6 и Firefox 3 [Перезалив с YouTube]](https://rutube.ru/video/3cf879626dfd57b5c7bccea2099dd0c3/)
