# Лабораторная работа 3: Внедрение Dependency Injection и SQLAlchemy в Litestar

## Структура проекта

\\\
app/
├── controllers/
│   └── user_controller.py     # HTTP endpoints
├── services/
│   └── user_service.py        # Бизнес-логика
├── repositories/
│   └── user_repository.py     # Работа с БД
├── models/                    # SQLAlchemy модели
│   └── adress.py  
│   └── order.py 
│   └── product.py  
│   └── user.py                 
├── schemas/
│   └── user_schema.py         # Pydantic схемы
└── main.py                    # Точка входа приложения
\\\

## Установка и запуск

### 1. Установка зависимостей

\\\bash
pip install -r requirements.txt
\\\

### 2. Настройка базы данных PostgreSQL

Установить PostgreSQL и создать базу данных:

\\\bash
# Подключитесь к PostgreSQL
psql -U postgres

# Создать базу данных
CREATE DATABASE lab_2;

# Создать пользователя
CREATE USER user WITH PASSWORD 'password';

# Предоставить права
GRANT ALL PRIVILEGES ON DATABASE lab_2 TO user;
\\\

### 3. Настройка переменных окружения

Скопировать `.env.example` в `.env` и изменить параметры подключения:

\\\bash
cp .env.example .env
\\\

Отредактируйте `.env`:
\\\
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/lab_2
\\\

### 4. Запуск приложения

\\\bash
python app/main.py
\\\

Или с помощью uvicorn:

\\\bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
\\\

## Использование API

### Документация API

После запуска приложения документация доступна по адресу:
- Swagger UI: http://localhost:8000/schema/swagger
- OpenAPI Schema: http://localhost:8000/schema/openapi.json

### Примеры запросов

#### 1. Создать пользователя (POST /users)

\\\bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john.doe@example.com",
    "description": "very good"
  }'
\\\

#### 2. Получить пользователя по ID (GET /users/{user_id})

\\\bash
curl http://localhost:8000/users/1
\\\

#### 3. Получить список пользователей с пагинацией (GET /users)

\\\bash
# Получить первые 10 пользователей (страница 1)
curl "http://localhost:8000/users?count=10&page=1"

# Получить следующие 10 пользователей (страница 2)
curl "http://localhost:8000/users?count=10&page=2"
\\\

#### 4. Обновить пользователя (PUT /users/{user_id})

\\\bash
curl -X PUT http://localhost:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.updated@example.com",
    "description": "very good"
  }'
\\\

#### 5. Удалить пользователя (DELETE /users/{user_id})

\\\bash
curl -X DELETE http://localhost:8000/users/1
\\\

## Работа с Git

### Создание тега для лабораторной работы 2

Перед началом работы создайте тег для предыдущей лабораторной:

\\\bash
git tag lab_2
git push origin lab_2
\\\

### Завершение лабораторной работы 3

После завершения работы создайте тег:

\\\bash
git add .
git commit -m "Completed lab 3"
git tag lab_3
git push origin main
git push origin lab_3
\\\

## Задание со звездочкой

Реализовано в методе `get_all_users()`:
- Возвращает список пользователей и их общее количество
- Помогает реализовать пагинацию на клиенте

## HTTP статусы

- **200 OK** - Успешный GET/PUT
- **201 Created** - Успешный POST (создание)
- **204 No Content** - Успешный DELETE
- **400 Bad Request** - Невалидные данные
- **404 Not Found** - Ресурс не найден
- **500 Internal Server Error** - Ошибка сервера
