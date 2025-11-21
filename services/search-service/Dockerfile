FROM python:3.11-slim    
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt  
COPY src/ .
# Указываем переменные окружения для Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000
ENV PYTHONUNBUFFERED=1

# Пробрасываем порт наружу
EXPOSE 8000

# Запуск Flask напрямую (так перезапуск и дебаг работают корректно)
CMD ["flask", "run"]