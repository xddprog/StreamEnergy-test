# Stream Energy Test Task
Тестовое задание в команию СтримЭнерджи
Ссылка на Телеграмм бота - 

## Используемые Backend технологии:
1. **FastAPI**  
2. **SQLAlchemy**  
4. **PostgreSQL**

## Возможности проекта:
- Создание, редактирование и удаление записей
- Получение записей по тегам
- Телеграмм бот для удобного взаимодействия с API

## Запуск проекта
1. Склонируйте репозиторий
```
git clone https://github.com/xddprog/StreamEnergy-test.git
```
2.1 Запуск с помощью docker
```
docker-compose build && docker-compose up -d
```
2.2 Локальный запуск
```
uvicorn app.main:app --reload && python tg_bot/bot.py
```

## Будущие возможности:
- Добавление веб-интерфейса или Telegramm WebApp
- Добавление ассинхронных запросов(в данный момент с библиотекой requests_async некорректно работает docker)
