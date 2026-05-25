# Week 17: Финальный микросервисный проект

## Что это
Проект `likes-s18` состоит из 3 сервисов на FastAPI:
1. `user-service` - работа с пользователями.
2. `post-service` - работа с постами.
3. `like-service` - работа с лайками и gRPC-сервис для подсчета лайков.

Взаимодействие:
1. Внешние клиенты используют REST API.
2. `post-service` обращается в `like-service` по gRPC (`GetLikesCount`), чтобы вернуть `likes_count` в ответе по посту.

Подробное описание: `weeks/week-17/ARCHITECTURE.md`

## Структура
1. Код сервисов: `weeks/week-17/app/`
2. Docker Compose: `weeks/week-17/app/docker-compose.yml`
3. Прото-контракт gRPC: `weeks/week-17/app/proto/likes.proto`
4. Архитектура: `weeks/week-17/ARCHITECTURE.md`

## Быстрый запуск
Требования:
1. Docker + Docker Compose
2. Свободные порты `8001`, `8002`, `8003`, `50051`

Запуск:
```bash
docker compose -f weeks/week-17/app/docker-compose.yml up -d --build
```

Остановка:
```bash
docker compose -f weeks/week-17/app/docker-compose.yml down -v
```

## Порты сервисов
1. `like-service` REST: `http://localhost:8001`
2. `like-service` gRPC: `localhost:50051`
3. `post-service` REST: `http://localhost:8002`
4. `user-service` REST: `http://localhost:8003`

## Health checks
1. `GET /health` реализован в каждом API-сервисе:
   - `http://localhost:8001/health`
   - `http://localhost:8002/health`
   - `http://localhost:8003/health`
2. Внутри endpoint-а выполняется проверка БД (`SELECT 1`).
3. В `docker-compose.yml` настроены container healthcheck-и для API и PostgreSQL.

## Примеры запросов
Создать пост:
```bash
curl -X POST "http://localhost:8002/posts?title=Hello&content=World"
```

Получить пост с `likes_count` (внутри выполнится gRPC-вызов):
```bash
curl "http://localhost:8002/posts/1"
```

Поставить лайк:
```bash
curl -X POST "http://localhost:8001/likes?post_id=1"
```

Создать пользователя:
```bash
curl -X POST "http://localhost:8003/users?email=user@example.com&password=123456"
```

## Локальная проверка
```bash
make test WEEK=17
```

## CI
Добавлен workflow: `.github/workflows/week-17-ci.yml`

Что делает CI:
1. Устанавливает Python зависимости.
2. Запускает `make test WEEK=17`.
3. Поднимает сервисы через Docker Compose.
4. Выполняет smoke-тест:
   - проверяет доступность gRPC порта `50051` у `like-service`;
   - проверяет сценарий `post-service -> gRPC -> like-service`;
   - опирается на readiness контейнеров через healthcheck.
5. Показывает логи при падении и останавливает контейнеры.
