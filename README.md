## Описание
API для отслеживания количества объявлений на avito.

Стек технологий:
- Fast API
- SqlAlchemy
- Beautifulsoup
- Postgres
- Docker
- Pytest

## Запуск
1. Клонировать репозиторий, перейти в директорию `src`

        cd avito_api/src

2. Запустить контейнер docker

        docker-compose up

3. Открыть api в браузере

        http://localhost:8002/docs

4. Запуск тестов

        docker-compose exec web pytest --cov=app/api

