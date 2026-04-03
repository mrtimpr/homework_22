# Django Catalog Project

Учебный проект на Django с приложением `catalog`.

Проект реализует базовый каталог товаров с подключением PostgreSQL, моделями категорий и продуктов, административной панелью, фикстурами, кастомной командой для загрузки тестовых данных и страницами `Главная` и `Контакты`, оформленными с помощью Bootstrap.

## Что реализовано

- инициализирован Django-проект;
- создано приложение `catalog`;
- приложение зарегистрировано в `INSTALLED_APPS`;
- настроена маршрутизация проекта и приложения через `include()`;
- используются шаблоны:
  - главная страница;
  - страница контактов;
- Bootstrap подключен локально через статические файлы проекта;
- на странице контактов реализована форма обратной связи;
- при `POST`-запросе данные формы выводятся в консоль сервера и пользователю показывается сообщение об успешной отправке;
- проект переведен с SQLite на PostgreSQL;
- параметры подключения к базе данных вынесены в переменные окружения `.env`;
- создан шаблон файла `.env.example`;
- созданы модели:
  - `Category`;
  - `Product`;
- для моделей настроены:
  - `verbose_name` и `verbose_name_plural`;
  - методы `__str__`;
  - связь `ForeignKey` между продуктом и категорией;
- выполнены миграции для моделей;
- настроены `MEDIA_URL` и `MEDIA_ROOT` для работы с изображениями продуктов;
- модели зарегистрированы в административной панели Django;
- для админки настроены:
  - вывод списков полей;
  - фильтрация продуктов по категории;
  - поиск по полям `name` и `description`;
- подготовлены фикстуры для категорий и продуктов;
- реализована кастомная команда `seed_catalog` для очистки базы и загрузки тестовых данных из фикстур;
- для работы с shell используется `ipython`.

## Основные модели

### Category

Содержит:
- `name` — наименование категории;
- `description` — описание категории.

### Product

Содержит:
- `name` — наименование продукта;
- `description` — описание продукта;
- `image` — изображение продукта;
- `category` — категория продукта;
- `price` — цена за покупку;
- `created_at` — дата создания;
- `updated_at` — дата последнего изменения.

## Структура проекта

```text
.
├── .env.example
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
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── fixtures/
│   │   ├── categories.json
│   │   └── products.json
│   ├── management/
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── seed_catalog.py
│   └── templates/
│       └── catalog/
│           ├── base.html
│           ├── contacts.html
│           └── home.html
├── media/
├── static/
│   └── bootstrap/
│       └── css/
│           └── bootstrap.min.css
├── shell_interaction_1.png
├── shell_interaction_2.png
└── .env
```

## Маршруты

- `/` — главная страница;
- `/contacts/` — страница контактов;
- `/admin/` — административная панель Django.

## Используемые технологии

- Python 3.14
- Django
- PostgreSQL
- psycopg2-binary
- Pillow
- IPython
- Bootstrap 5
- HTML

## Установка и запуск проекта

### 1. Клонировать репозиторий

```bash
git clone <ссылка_на_репозиторий>
cd homework_22
```

### 2. Создать и активировать виртуальное окружение

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

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Создать базу данных PostgreSQL

Базу данных нужно создать заранее вручную, например:

```sql
CREATE DATABASE homework_22;
```

### 5. Настроить переменные окружения

Создайте файл `.env` в корне проекта по шаблону `.env.example`.

Пример содержимого:

```env
DJANGO_SECRET_KEY=твой-реальный-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

POSTGRES_DB=homework_22
POSTGRES_USER=postgres
POSTGRES_PASSWORD=твой_пароль
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

### 6. Применить миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Создать суперпользователя

```bash
python manage.py createsuperuser
```

### 8. Запустить сервер

```bash
python manage.py runserver
```

После запуска проект будет доступен по адресу:

```text
http://127.0.0.1:8000/
```

## Работа с административной панелью

После создания суперпользователя открой:

```text
http://127.0.0.1:8000/admin/
```

В административной панели доступны модели:
- `Category`;
- `Product`.

Для `Category` отображаются поля:
- `id`;
- `name`.

Для `Product` отображаются поля:
- `id`;
- `name`;
- `price`;
- `category`.

Также настроены:
- фильтрация продуктов по категории;
- поиск по `name` и `description`.

Скриншоты примера взаимодействия добавленны в проект:
- shell_interaction_1.png
- shell_interaction_2.png

## Работа с фикстурами

Загрузка категорий:

```bash
python manage.py loaddata catalog/fixtures/categories.json
```

Загрузка продуктов:

```bash
python manage.py loaddata catalog/fixtures/products.json
```

## Кастомная команда

Команда `seed_catalog`:
- удаляет существующие категории и продукты;
- загружает новые данные из фикстур.

Запуск:

```bash
python manage.py seed_catalog
```

## Работа с shell

Запуск Django shell с IPython:

```bash
python manage.py shell -i ipython
```

Примеры ORM-запросов:

```python
from catalog.models import Category, Product

smartphones = Category.objects.create(
    name='Смартфоны',
    description='Мобильные устройства',
)

tv = Category.objects.create(
    name='Телевизоры',
    description='Устройства для дома',
)

iphone = Product.objects.create(
    name='iPhone 15',
    description='Смартфон Apple',
    category=smartphones,
    price=99990.00,
)

Category.objects.all()
Product.objects.all()
Product.objects.filter(category=smartphones)
```

## Работа формы обратной связи

На странице `/contacts/` доступна форма с полями:
- имя;
- контактный телефон;
- сообщение.

После отправки формы:
- Django получает `POST`-запрос;
- данные формы печатаются в консоль сервера;
- пользователю показывается сообщение об успешной отправке.

## Работа с медиаданными

Изображения продуктов сохраняются в директорию `media/`.

В режиме разработки медиаданные доступны через настройки:
- `MEDIA_URL`;
- `MEDIA_ROOT`.