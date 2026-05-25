FROM python:3.12

WORKDIR /app

COPY ./post_service/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./post_service /app
COPY ./proto /app/proto

CMD ["python", "-m", "uvicorn", "posts:app", "--host", "0.0.0.0", "--port", "8000"]