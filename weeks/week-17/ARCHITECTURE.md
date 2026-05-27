# Архитектура финального проекта (Week 17)

## Проект и вариант
- `project_code`: **likes-s18**
- Тема варианта: сервис лайков (`resource = likes`)

## Обзор системы
Система состоит из 3 микросервисов:
1. `user-service` - управление пользователями.
2. `post-service` - управление постами и выдача поста с количеством лайков.
3. `like-service` - управление лайками и gRPC-метод получения количества лайков по `post_id`.

У каждого сервиса своя отдельная БД PostgreSQL:
1. `user-db`
2. `post-db`
3. `like-db`

Такой подход снижает связность между сервисами и упрощает независимое развитие.

## Взаимодействие сервисов
1. Внешний клиент работает с HTTP API сервисов (REST).
2. `post-service` при запросе `GET /posts/{post_id}` выполняет внутренний gRPC-вызов в `like-service` (`GetLikesCount`), чтобы вернуть `likes_count` вместе с постом.

Схема:

`Client -> REST -> post-service -> gRPC -> like-service -> like-db`

## Протоколы и причины выбора
1. REST (FastAPI) для внешнего API:
   - удобен для ручного тестирования и интеграции с фронтендом;
   - хорошо читаемые JSON-ответы.
2. gRPC для межсервисного вызова `post-service -> like-service`:
   - строгий контракт через `.proto`;
   - быстрый и компактный бинарный протокол для внутреннего взаимодействия.

## Контейнеризация и локальный запуск
Локальная инфраструктура описана в `docker-compose.yml`:
1. Поднимаются 3 API-сервиса и 3 PostgreSQL.
2. Проброшены порты:
   - `like-service`: `8001` (REST) и `50051` (gRPC),
   - `post-service`: `8002`,
   - `user-service`: `8003`.

Запуск выполняется одной командой:

```bash
docker compose -f weeks/week-17/app/docker-compose.yml up --build
```

## Kubernetes-деплой
Для кластера добавлены манифесты в `weeks/week-17/k8s`:
1. `namespace.yaml` - namespace `likes-s18`.
2. Три PostgreSQL (Deployment + Service): `like-db`, `post-db`, `user-db`.
3. Три API (Deployment + Service): `like-service`, `post-service`, `user-service`.

DNS-имена сервисов в Kubernetes совпадают с хостами в коде (`like-db`, `post-db`, `user-db`, `like-service`), поэтому приложение запускается без изменений Python-кода.

Применение:

```bash
kubectl apply -f weeks/week-17/k8s/namespace.yaml
kubectl apply -f weeks/week-17/k8s/
```

## Отказоустойчивость и связность
1. Если gRPC недоступен, `post-service` не падает: в обработчике исключения возвращает `likes_count = 0`.
2. Сервисы разделены по данным (разные БД), поэтому сбой одной БД не ломает все домены сразу.

## Наблюдаемость
1. Базовое логирование реализовано через stdout/stderr контейнеров.
2. В каждом API реализован endpoint `GET /health` с проверкой доступности БД (`SELECT 1`).
3. В `docker-compose.yml` настроены `healthcheck`:
   - для API-сервисов через вызов `http://127.0.0.1:8000/health`,
   - для Postgres через `pg_isready`.
4. `depends_on` использует `condition: service_healthy`, поэтому API стартуют только после готовности своих БД.
5. Логи доступны через:

```bash
docker compose -f weeks/week-17/app/docker-compose.yml logs -f
```

## CI/CD
Настроен workflow `.github/workflows/week-17-ci.yml`. Он выполняет:
1. Установка зависимостей.
2. Запуск тестов (`make test WEEK=17`).
3. Подъем сервисов через Docker Compose.
4. Smoke-проверку:
   - открыт ли gRPC порт `50051` у `like-service`,
   - работает ли сценарий `post-service -> gRPC -> like-service`.
5. Сбор логов при ошибке и корректное завершение окружения (`down -v`).

Для этапа Continuous Delivery добавлен `.github/workflows/week-17-cd.yml`:
1. Переиспользует тесты как quality gate.
2. Собирает и публикует три сервисных образа в GHCR с тегом `${GITHUB_SHA}`.
3. Применяет Kubernetes-манифесты (`kubectl apply`).
4. Обновляет образы в Deployments через `kubectl set image`.
5. Ждет завершения rolling update через `kubectl rollout status`.

Таким образом, изменение в `main` проходит путь: тесты -> публикация образов -> автоматический деплой в кластер.
