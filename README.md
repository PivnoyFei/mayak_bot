![Build Status](https://github.com/PivnoyFei/mayak_bot/actions/workflows/main.yml/badge.svg?branch=main)

## Тестовое задание Python
#### Представьте, что вас есть система без интерфейса пользователя, например краулер (сборщик информации), который парсит все сайты по продаже зюзюбликов и сохраняет в базу данных.

#### Появилась потребность дать обычному пользователю минимальными усилиями добавлять еще сайты для парсинга
#### Напишите простого бота, который будет иметь одну кнопку: загрузить файл
- При нажатии кнопки пользователь прикрепляет файл excel в формате (название, URL, xpath запрос)
- Бот получает файл, сохраняет
- Открывает файл библиотекой pandas
- Выводит содержимое в ответ пользователю
- Сохраняет содержимое в локальную бд sqlite
#### Реализация на python, решение должно быть представлено ссылкой на репозиторий и на бота (как основной вариант телеграм, но возможно вы предложите что-то еще).
#### Внутри репозитория должна быть инструкция по развёртыванию и корректный файл с необходимыми зависимостями (requerments, pipenv, poetry на ваш выбор)

#### Задание рассчитано на один день, выполнять можно в удобное время в течении недели
#### Задача со *: провести парсинг по данным из таблицы и вывести среднюю цену зюзюблика по каждому сайту. В качестве зюзюблика можете взять любой интересный вам товар

### Стек: 
```
Python 3.11, aiogram 2.24.
```

### Запуск проекта
Клонируем репозиторий и переходим в него:
```bash
git clone https://github.com/PivnoyFei/mayak_bot
cd mayak_bot
```
#### Создаем и активируем виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate
```
#### для Windows
```bash
python -m venv venv
source venv/Scripts/activate
```

#### Обновиляем pip и ставим зависимости из req.txt:
```bash
python -m pip install --upgrade pip && pip install -r requirements.txt
```
#### Создаем файл .env, добавляем TOKEN бота в .env
```bash
TOKEN = 'key'
DATABASE_URL = 'sqlite:///sqlite3.db' 
```
#### Миграции базы данных (не обязательно):
```bash
alembic revision --message="Initial" --autogenerate
alembic upgrade head
```
#### Запускаем проект:
```bash
python main.py
```
