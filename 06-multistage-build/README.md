# Урок 6. Многоэтапная сборка, контекст сборки

## Контекст сборки

**Контекст сборки** - это набор файлов, к которым ваша сборка может получить доступ.

Контекстом сборки может быть локальный каталог, Git-репозиторий или tar-архив.

В этом случае, доступные в контексте сборки файлы - это все файлы из локального каталога, git-репозитория или содержимое tar-архива.

Инструкции `COPY` и `ADD` могут работать с любыми файлами и каталогами в контексте.

Вы можете использовать `.dockerignore` файл для исключения файлов или каталогов из контекста сборки.

Это помогает избежать отправки нежелательных файлов и каталогов в конструктор, повышая скорость сборки, особенно при использовании удаленного конструктора.

## Пример запуска React приложения в Docker контейнере

### Инициализация проекта на React

```shell
docker run --rm -ti \
    -u $(id -u):$(id -g) \
    -e HOME=/tmp \
    -v "$(pwd):/src" \
    -w /src \
    node:20.14-bookworm-slim \
        npx create-react-app app

# или с помощью Vite, но команды запуска сервера, сборки и т.д. другие - нужно править Dockerfile
docker run --rm -ti \
    -u $(id -u):$(id -g) \
    -e HOME=/tmp \
    -v "$(pwd):/src" \
    -w /src \
    node:20.14-bookworm-slim \
        sh -c 'npm create vite@latest . -- --template react && npm install'
```

### Команды для работы с образом

```shell
# Сборка версии образа для среды разработки
docker build -t example-react -f Dockerfile --target development ./app

# Запуск контейнера в среде разработки
docker run --rm -ti \
    --name react_1 \
    -p "127.0.0.1:3000:3000" \
    -v "$(pwd)/app:/app" \
    example-react

# Сборка версии образа для производственной среды
docker build -t example-react -f Dockerfile ./app

# Запуск контейнера в производственной среде
docker run --rm -ti --name react_1 -p "3000:80" example-react
```

## Пример запуска программы ipclassifier

`ipclassifier` - это консольная программу на C++, которая принимает один позиционный аргумент IP-адрес и выводит на экран к какому классу сетей он относится. [Программу написал ChatGPT](https://chatgpt.com/share/54469448-66d6-44ac-bfee-64f6b20ed30a).

### Команды для работы с образом

```shell
# Сборка образа с программой
docker build -t ipclassifier -f Dockerfile ./src

# Использование "временного" контейнера для запуска программы
docker run --rm ipclassifier 127.0.0.1
docker run --rm ipclassifier 192.168.88.1
docker run --rm ipclassifier
```

## Ссылки

* [Docker docs - Build context](https://docs.docker.com/build/building/context/)
* [Docker docs - Multi-stage](https://docs.docker.com/build/guide/multi-stage/)
* [.gitignore docs](https://git-scm.com/docs/gitignore)
* [React Framework](https://react.dev/)
* [Create React App](https://create-react-app.dev/)
* [Scaffolding Your First Vite Project](https://vitejs.dev/guide/#scaffolding-your-first-vite-project)

