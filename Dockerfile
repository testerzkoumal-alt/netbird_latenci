FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn redis
CMD ["python", "main.py"]