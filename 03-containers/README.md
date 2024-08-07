# Урок 3. Контейнеры

- [Изученные команды](#изученные-команды)
- [Ссылки](#ссылки)

**Контейнер** - это фактически запущенный в изолированной среде образ.
Для запущенного контейнера создается новый слой с возможностью изменения данных.
Данные сохраняются до момента, пока контейнер не будет удален.

На базе одного образа можно создать множество контейнеров
и запустить их на разных машинах, но не забываем главное правило -
хостовая ОС должна совпадать с ОС контейнера.

## Изученные команды

```bash
# Команды для управления контейнерами Docker
docker container

# Список запущенных контейнеров
docker ps
# Список всех контейнеров
docker ps -a

# Старт контейнера на базе самого свежего образа debian
docker run debian
# Задать имя контейнеру при старте
docker run --name test_1 debian
# -t: создает псевдо-терминал внутри контейнера,
# что позволяет вам взаимодействовать с командной строкой в контейнере,
# так же, как если бы он был локальным компьютером.
# Без этой опции процесс в контейнере может не получать ввод с клавиатуры.
#
# -i: позволяет делать ввод с клавиатуры в контейнер, основанный на стандартном потоке вводе (stdin),
# позволяя, например, передавать данные из вашего текущего сеанса в контейнер
# или вводить команды в интерактивном режиме.
# 
# Обычно обе эти опции используются вместе для взаимодействия с контейнером через терминал.
docker run --name test_2 -ti debian

# Запуск контейнера в фоновом режиме (как демона)
docker run --name test_3 -ti -d debian

# Остановить запущенный контейнер
docker stop test_2

# Старт ранее остановленного контейнера
docker start test_2

# Перезапуск запущенного контейнера
docker restart test_3

# Выполнение команды в запущенном контейнере
# "логин" в контейнере - запуск оболочки
docker exec -ti test_2 bash
# создать файл test_2.txt в корне контейнера test_2
docker exec -ti test_2 touch test_2.txt
# просмотр файлов в корне контейнера test_2
docker exec -ti test_2 ls
# создать файл test_3.txt в корне контейнера test_3
docker exec -ti test_3 touch test_3.txt

# Копирование файла из контейнера на хост
docker cp test_2:/test_2.txt test_2.txt
# Копирование файла с хоста в контейнер
docker cp test_2.txt test_3:/test_2.txt
# Копирование между контейнерами не поддерживается
docker cp test_3:/test_3.txt test_2:/test_3.txt
# Однако можно выполнить копирование через STDOUT-STDIN
docker cp test_3:/test_3.txt - | docker cp - test_2:/

# Просмотр информации о запущенном контейнере
docker inspect test_2 | less

# Просмотр процессов в запущенном контейнере
docker top test_2
# a: выводить информацию о процессах для всех пользователей.
# Без этого аргумента ps выводит информацию только о процессах текущего пользователя.
#
# x: выводить информацию о процессах, не связанных с терминалом.
# Он позволяет отображать процессы, запущенные в фоновом режиме или вне сеанса пользователя.
#
# f: выводить древовидное представление процессов.
# Он позволяет видеть отношения между процессами,
# например, какой процесс является родителем для каких процессов-потомков.
#
# u: выводить расширенную информацию о процессах.
# Он включает в вывод дополнительные поля,
# такие как пользователь, от которого запущен процесс, и время его запуска.
docker top test_2 axfu

# Просмотр потребляемых контейнером ресурсов
docker stats
# в том числе для остановленных контейнеров
docker stats -a
# для указанных контейнеров
docker stats test_2 test_3
# показать и выйти
docker stats --no-stream test_2

# Удалить контейнер
docker rm test_1
# или более одного
docker rm test_2 test_3

# Удалить все остановленные контейнеры
docker container prune

# Удалить не используемые Docker данные
docker system prune
docker system prune -a
docker system prune --volumes -a
```

## Ссылки

* [man ps](https://www.man7.org/linux/man-pages/man1/ps.1.html)
* [man signal](https://www.man7.org/linux/man-pages/man7/signal.7.html)
