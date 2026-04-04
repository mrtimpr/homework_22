# Django Catalog Project

Проект на Django с приложением `catalog`, домашней страницей и страницей контактов.

## Что реализовано

- инициализирован Django-проект;
- создано приложение `catalog`;
- приложение зарегистрировано в `INSTALLED_APPS`;
- настроена маршрутизация проекта и приложения;
- подготовлены два HTML-шаблона:
  - главная страница;
  - страница контактов;
- для стилизации используется Bootstrap;
- Bootstrap подключен локально через статические файлы проекта;
- на странице контактов реализована форма обратной связи;
- при POST-запросе:
  - данные формы выводятся в консоль сервера;
  - на странице отображается сообщение об успешной отправке.

## Структура проекта

```text
.
├── .gitignore
├── README.md
├── manage.py
├── requirements.txt
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── catalog/
│   ├── __init__.py
│   ├── apps.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── catalog/
│           ├── base.html
│           ├── contacts.html
│           └── home.html
└── static/
    └── bootstrap/
        └── css/
            └── bootstrap.min.css
```

## Маршруты

- `/` — главная страница;
- `/contacts/` — страница контактов.

## Запуск проекта

### 1. Создать и активировать виртуальное окружение

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Выполнить миграции

```bash
python manage.py migrate
```

### 4. Запустить сервер

```bash
python manage.py runserver
```

После запуска проект будет доступен по адресу:

```text
http://127.0.0.1:8000/
```

## Работа формы обратной связи

На странице `/contacts/` доступна форма с полями:

- имя;
- контактный телефон;
- сообщение.

После отправки формы:

- Django получает `POST`-запрос;
- данные формы печатаются в консоль сервера;
- пользователю показывается сообщение: `Сообщение успешно отправлено.`

## .gitignore

В проекте добавлен `.gitignore`, в котором учтены:

- `.idea`;
- `venv`;
- `env`;
- `__pycache__`;
- базы данных `sqlite`.

## Используемые технологии

- Python
- Django
- Bootstrap 5
- HTML
- CSS