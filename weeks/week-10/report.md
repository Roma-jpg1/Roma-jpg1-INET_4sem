# Отчет по Docker

В этом месте вам необходимо:
- Размер образа 126MB
- Количество слоёв
    - `FROM python:3.11-slim AS builder` создает stage для установки зависимостей
    - `COPY requirements.txt .` создает отдельный слой и позволяет использовать кэш
    - `RUN pip install --prefix=/install -r requirements.txt` создает слой с зависимостями
    - `COPY --from=builder /install /usr/local` переносит зависимости в финальный образ
    - `COPY . .` добавляет файлы приложения отдельным слоем
- Команды сборки/запуска
    - docker build -t week10-app .
    - docker run -p 8188:8188 week10-app