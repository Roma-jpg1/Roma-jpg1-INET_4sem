FROM python:3.12

WORKDIR /app

COPY ./user_service/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./user_service /app

CMD ["python", "-m", "uvicorn", "users:app", "--host", "0.0.0.0", "--port", "8000"]