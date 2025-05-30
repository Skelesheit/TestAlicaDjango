FROM python:3.12-slim

WORKDIR /app

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "TestAlicaDj.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--workers", "6", "--threads", "2", "--bind", "0.0.0.0:8000"]
