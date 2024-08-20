# GitHub Actions

- [Запуск задач локально](#запуск-задач-локально)
  - [Установка](#установка)
  - [Переменные и секреты](#переменные-и-секреты)
  - [Запуск](#запуск)
- [Ссылки](#ссылки)

Чтобы автоматически обновлять версии для используемых действий (action) воспользуйтесь Dependabot.
В директории `.github` создайте файл с именем `dependabot.yml` и добавьте следующую конфигурацию:

```yaml
# Версия конфигурации dependabot
version: 2

updates:
  # Экосистема пакетов, для которой будут проверяться обновления
  - package-ecosystem: "github-actions"
    # Директория, в которой dependabot будет искать файл конфигурации
    directory: "/"
    schedule:
      # Частота проверки обновлений (еженедельно)
      interval: "weekly"
```

## Запуск задач локально

GitHub Actions workflows можно запускать локально для отладки с помощью инструмента [act](https://nektosact.com/introduction.html).

### Установка

Для установки в Linux/MacOS выполните команду:

```shell
wget -qO- https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash /dev/stdin -b /usr/local/bin
```

В Windows переходим по [ссылке](https://github.com/nektos/act/releases/latest) и скачиваем нужную версию, распаковываем архив в любую удобную директорию,
опционально добавляем эту директорию в переменную окружения `PATH`.

### Переменные и секреты

Скорее всего вам понадобится токен доступа для Github, создать его можно по [ссылке](https://github.com/settings/tokens).
Синтаксис файлов для хранения секретов или переменных эквивалентен синтаксису файлов с переменными окружения, например:

```
GITHUB_TOKEN=...
DOCKER_HUB_USERNAME=...
DOCKER_HUB_ACCESS_TOKEN=...
```

Команда запуска будет выглядеть так:

```shell
act --var-file <PATH_TO_YOUR_FILE> --secret-file <PATH_TO_YOUR_FILE>
```

### Запуск

Если не указан [тип события](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows),
то будет использован `push`:

```shell
# Запуск всех задач, -C директория проекта, по умолчанию текущая 
act -C <PATH_TO_YOUR_REPOSITORY_DIR>

# Запуск указанной задачи
act --var-file <PATH_TO_YOUR_FILE> \
    --secret-file <PATH_TO_YOUR_FILE> \
    -W .github/workflows/dockerhub-image.yml

# Запуск указанной задачи для события Pull Request
act pull_request \
    --var-file <PATH_TO_YOUR_FILE> \
    --secret-file <PATH_TO_YOUR_FILE> \
    -W .github/workflows/dockerhub-image.yml
```

## Ссылки

* [Документация GitHub Actions](https://docs.github.com/ru/actions)
* [Introduction to GitHub Actions](https://docs.docker.com/build/ci/github-actions/)
* [act](https://nektosact.com/introduction.html)
