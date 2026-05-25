FROM python:3.12

WORKDIR /app

COPY ./like_service/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./like_service /app


COPY ./like_service /app
COPY ./proto /app/proto

CMD ["python", "-m", "uvicorn", "likes:app", "--host", "0.0.0.0", "--port", "8000"]