# Менеджер задач

Простое веб-приложение для управления задачами с авторизацией пользователей.

## Технологии

### Backend
- **FastAPI** - Python фреймворк для создания API
- **PostgreSQL** - реляционная база данных
- **SQLAlchemy** - ORM для работы с БД

### Frontend
- **HTML** - разметка страницы
- **CSS** - стилизация
- **JavaScript** - интерактивность

## Функционал

### Управление пользователями
- Регистрация новых пользователей
- Авторизация с защитой доступа

### Работа с задачами
- Просмотр списка задач
- Добавление новых задач
- Редактирование существующих задач
- Удаление задач

### Организация задач
- Фильтрация по:
  - Статусу
  - Дате
  - Комбинации критериев

## Структура задачи
Каждая задача содержит:
- Название (`title`)
- Описание (`description`)
- Статус (`status`)

Автоматически генерируются:
- Уникальный ID
- Дата создания

## Безопасность
- Доступ только к собственным задачам пользователя
- Хеширование паролей с использованием `bcrypt` + соль
- Аутентификация через JWT-токены

## Интерфейс
- **Добавление задачи**: кнопка "Добавить" → модальное окно
- **Редактирование**: клик по задаче → модальное окно
- **Удаление**: кнопка "удалить" рядом с задачей
- **Фильтрация**: панель фильтров → кнопка "Применить"

## Описание API Endpoints

### Аутентификация и регистрация

#### `POST /login`
- **Описание**: Вход пользователя в систему
- **Параметры**:
  - `login_user` (form): Логин пользователя
  - `password` (form): Пароль
- **Возвращает**: JWT токен в cookies
- **Коды ответа**:
  - 200: Успешный вход
  - 401: Неверные учетные данные

#### `POST /logout`
- **Описание**: Выход пользователя из системы
- **Действие**: Удаляет access_token cookie
- **Возвращает**: Сообщение об успешном выходе

#### `POST /register`
- **Описание**: Регистрация нового пользователя
- **Параметры**:
  - `login_user` (form): Логин
  - `email` (form): Email
  - `password` (form): Пароль
  - `password_confirm` (form): Подтверждение пароля
- **Коды ответа**:
  - 201: Успешная регистрация
  - 400: Пароли не совпадают

### Работа с задачами

#### `GET /`
- **Описание**: Главная страница приложения
- **Возвращает**: HTML шаблон index.html

#### `GET /tasks_of_user/{user_id}`
- **Описание**: Получение задач конкретного пользователя
- **Параметры**:
  - `user_id` (path): ID пользователя
- **Проверка**: Сверяет user_id с JWT токеном
- **Возвращает**: HTML шаблон tasks.html с задачами

#### `GET /tasks`
- **Описание**: Получение всех задач (с фильтрацией по статусу)
- **Параметры**:
  - `status` (query): Фильтр по статусу задачи
- **Требуется**: JWT токен
- **Возвращает**: Список задач

#### `GET /tasks/{task_id}`
- **Описание**: Получение конкретной задачи
- **Параметры**:
  - `task_id` (path): ID задачи
- **Требуется**: JWT токен
- **Коды ответа**:
  - 200: Задача найдена
  - 404: Задача не найдена

#### `POST /tasks/create`
- **Описание**: Создание новой задачи
- **Параметры** (form):
  - `user_id`: ID владельца
  - `title`: Название
  - `description`: Описание
  - `status`: Статус
- **Проверка**: Сверяет user_id с JWT токеном
- **Возвращает**: Созданную задачу

#### `PUT /tasks/{task_id}`
- **Описание**: Обновление существующей задачи
- **Параметры** (form):
  - `title`: Новое название
  - `description`: Новое описание
  - `status`: Новый статус
- **Требуется**: JWT токен
- **Коды ответа**:
  - 200: Задача обновлена
  - 404: Задача не найдена

#### `DELETE /tasks/{task_id}`
- **Описание**: Удаление задачи
- **Параметры**:
  - `task_id` (path): ID задачи
- **Требуется**: JWT токен
- **Возвращает**: Сообщение об успешном удалении
- **Коды ответа**:
  - 200: Задача удалена
  - 404: Задача не найдена


## Установка 
```bash
# Временно только на PyCharm, с докером не разобралась 

# Клонировать репозиторий
git clone https://github.com/VioNo/project.git

# Установить зависимости
pip install -r install.txt

# Поменять настройки в .env на соответствующие вашим, в своей бд запустить скрипт  
# Запустить приложение можно через команду 
python app/run.py
