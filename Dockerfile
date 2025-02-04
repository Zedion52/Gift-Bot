# Используем Python 3.11
FROM python:3.11

# Устанавливаем зависимости
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бота
COPY . .

# Запуск бота
CMD ["python", "bot.py"]
