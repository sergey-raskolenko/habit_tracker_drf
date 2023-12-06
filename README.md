# Учебный проект "Трекер привычек"

## Описание

Приложение для создания атомарных привычек по модели книги Джеймса Клира «Атомные привычки».
В рамках учебного курсового проекта реализована бэкенд-часть SPA веб-приложения.

### Регистрация и авторизация

Пользователи могут зарегистрироваться в системе и войти в свою учетную запись,
чтобы получить доступ к персонализированным функциям.

### Интеграция с Telegram

Настроена интеграция с мессенджером Telegram для рассылки уведомлений и напоминаний о выполнении привычки.

### Права доступа

* Каждый пользователь имеет доступ только к своим привычкам по механизму CRUD.
* Пользователь может видеть список публичных привычек без возможности их как-то редактировать или удалять.

### Пагинация

Реализована пагинация по 5 привычек на страницу, для удобства.

### Безопасность

Настроен CORS, чтобы фронтенд мог подключаться к проекту на развернутом сервере.

### Документация

Документация приложения содержит описание эндпоинтов и их работы.

## Используемые технологии

В разработке проекта использовались следующие технологии:

* **Python**: основной язык программирования проекта.
* **Django Rest Framework (DRF)**: основной фреймворк для разработки API.
* **PostgreSQL**: система управления базами данных, которая используется для хранения и обработки данных.
* **Redis**: используется как брокер сообщений для Celery.
* **Celery**: используется для обработки асинхронных задач, таких как отправка рассылок по электронной почте,
  отправка напоминаний в Telegram

## Запуск проекта

### Клонирование репозитория помощью консольной команды:
```bash
git clone <URL репозитория>
```
### Создать телеграм-бота, используя телеграм-бот @BotFather

### Настройка окружения. 
В директории проекта необходимо создать файл `.env` по примеру файла `.env.sample`


### Установка зависимостей
```bash
pip install -r requirements.txt
```
### Установка и настройка Redis
Установка
```bash
sudo apt-get install redis-server
```
Запуск
```bash
sudo service redis-server start
```
Для проверки работы, ответ: **PONG**
```bash
redis-cli ping
```
### Настройка окружения. 
В директории проекта необходимо создать файл `.env` по примеру файла `.env.sample`

### Команды ля запуска приложения с помощью Docker:
```bash
docker-compose up --build
```