#!/bin/bash

# Проверка наличия Docker
if ! command -v docker &> /dev/null; then
    echo "Docker не установлен. Пожалуйста, установите Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Проверка наличия Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose не установлен. Пожалуйста, установите Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

# Проверка существования файла .env
if [ ! -f ".env" ]; then
    echo "Файл .env не найден. Создайте его с параметрами:"
    echo "BOT_TOKEN=your_bot_token_here"
    echo "REDIS_HOST=redis"
    echo "REDIS_PORT=6379"
    exit 1
fi

# Сборка и запуск контейнеров
echo "Запускаем бота..."
docker-compose up --build