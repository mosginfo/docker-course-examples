# Урок 7. Контейнер, как исполняемый файл

## Exec form против Shell form

`RUN`, `CMD`, `ENTRYPOINT` имеют две возможные формы:

1. **exec form** - исполняемая форма
2. **shell form** - форма оболочки

Посмотреть информацию о `CMD` и `ENTRYPOINT`:
```shell
docker pull alpine
docker inspect --format '{{json .Config}}' alpine
```

### Исполняемая форма

Предподчительно для `CMD` и `ENTRYPOINT`:
```
INSTRUCTION ["executable","param1","param2"]
```

Превращается в:
```
executable param1 param2
```

1. Использует синтаксис массива JSON,
   поэтому все значения строго в двойных кавычках
2. Не использует оболочку, поэтому не работает, например:
   подстановка переменных окружения, перенаправление ввода/вывода,
   конвейеры, шаблоны подстановки имен файлов
3. Обратный слэш всегда экранируется - `\\`,
   иначе неявное приведение к форме оболочки

```dockerfile
# Не сработает, напечатает $HOME
CMD ["echo", "$HOME"]

# Не сработает, будет ошибка ls: cannot access '/lib*': No such file or directory
CMD ["ls", "-d", "/lib*"]

# Не сработает, посчитает > за позиционный аргумент
CMD ["whoami", ">", "/result.txt"]

# Не сработает, будет ошибка /bin/sh: [echo,: not found
CMD ["echo", "-e", "\033[1mBold text\033[0m"]

# Сработает, напечатает Bold text жирным
CMD ["echo", "-e", "\\033[1mBold text\\033[0m"]
```

```shell
# Пример с переменными окружения
docker build -t example-exec --target environ - < Dockerfile-exec
docker run --rm example-exec

# Пример с шаблонами имен файлов
docker build -t example-exec --target fpattern - < Dockerfile-exec
docker run --rm example-exec

# Пример с перенаправлением стандартных потоков
docker build -t example-exec --target pipe - < Dockerfile-exec
docker run --rm example-exec

# Пример с не экранированным слешем
docker build -t example-exec --target slash - < Dockerfile-exec
docker run --rm example-exec

# Пример с экранированием слешей
docker build -t example-exec - < Dockerfile-exec
docker run --rm example-exec
```


### Форма оболочки

Предподчительно для `RUN`:
```
INSTRUCTION command param1 param2
```

Превращается в:
```
/bin/sh -c 'executable param1 param2'
```

1. Разрешает использовать возможности оболочки, например:
   подстановка переменных окружения, перенаправление ввода/вывода,
   конвейеры, шаблоны подстановки имен файлов
2. Обратный слэш используется как метасимвол
   для многострочных команд и для экранирования.
   Если нужен символ обратного слэша - то экранируй `\\`

```dockerfile
# Сработает, напечатает /root
CMD echo "$HOME"

# Сработает, будут выведены имена файлов, начинающиеся с lib, в корневом каналоге
CMD ls -d /lib*

# Сработает, но смысла в этой команде нет =)
CMD whoami > /result.txt

# Сработает и напечатает Bold text жирным
CMD echo -e "\033[1mBold text\033[0m"

# Не сработает, ошибка /bin/sh: syntax error: unterminated quoted string 
CMD echo "\"

# Сработает, напечатает обратный слэш
CMD echo "\\"
```

```shell
# Пример с переменными окружения
docker build -t example-shell --target environ - < Dockerfile-shell
docker run --rm example-shell

# Пример с шаблонами имен файлов
docker build -t example-shell --target fpattern - < Dockerfile-shell
docker run --rm example-shell

# Пример с перенаправлением стандартных потоков
docker build -t example-shell --target pipe - < Dockerfile-shell
docker run --rm example-shell

# Пример с жирным шрифтом
docker build -t example-shell --target slash - < Dockerfile-shell
docker run --rm example-shell

# Пример с не экранированным слешем
docker build -t example-shell --target slash-error - < Dockerfile-shell
docker run --rm example-shell

# Пример с экранированием слешей
docker build -t example-shell - < Dockerfile-shell
docker run --rm example-shell
```


## CMD vs ENTRYPOINT

[Таблица из документации](https://docs.docker.com/reference/dockerfile/#understand-how-cmd-and-entrypoint-interact)

`ENTRYPOINT` должен быть определен если контейнер используется как исполняемый файл
или как скрипт настройки среды и запуска основного процесса внутри контейнера:

```shell
#!/usr/bin/env sh

# Например: 
# - установка переменных среды
# - проверка зависимостей
# - настройка конфигурационных файлов
# - обработка секретов
# - переключение пользователя/группы
# - патчинг пользователя/группы

# Запуск основного приложения
exec "$@"
```

`CMD` следует использовать для указания аргументов по-умолчанию для команды `ENTRYPOINT`
или для выполнения команды в контейнере.
`CMD` можно переопределить при запуске контейнера,
`ENTRYPOINT` тоже можно переопределить, но это менее удобно.
