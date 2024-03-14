## Виртуальная стажировка
Общая задача: Разработать мобильное приложение для Android и IOS, которое упростило бы туристам задачу по отправке данных о перевале и сократило время обработки запроса до трёх дней.

Задача: В соответствии с заданием разработать REST API, которое будет обслуживать мобильное приложение.

---

- Python 3.10
- Django 4.2
- Django REST framework 3.1
- PostgreSQL 15.4

---

Документация: http://127.0.0.1:8000/swagger/

Base URL: 127.0.0.1:8000/api/v1

### API endpoint-s:

POST, добавление записи о перевале в БД cо статусом "Новый"

    127.0.0.1:8000/api/v1/create/

GET, просмотр информации о перевале

    127.0.0.1:8000/api/v1/submitData/{id}

PUT, изменение статуса записи модератором

    127.0.0.1:8000/api/v1/update/{id}

GET, PUT, изменение (просмотр) записи пользователем, изменение возможно пока статус "Новый"

    127.0.0.1:8000/api/v1/submitData/update/{id}

GET, просмотр всех записей пользователя

    127.0.0.1:8000/api/v1/submitData/{email}/

GET, просмотр всех id записей

    127.0.0.1:8000/api/v1/perevals/

## Примеры:

Создание записи

    POST: 127.0.0.1:8000/api/v1/create/
    {
        "beauty_title": "Что-то красивое",
        "title": "Перевал",
        "other_titles": "Скиталец",
        "connect": "_",
        "users_id": {
            "full_name": "Иванов Иван Иванович",
            "email": "example@yandex.ru",
            "phone": "+79000000000"
        },
        "coord_id": {
            "latitude": 24.56,
            "longitude": 34.22,
            "height": 2200
        },
        "level_id": {
            "winter": "1А",
            "spring": "2А",
            "summer": "3Б",
            "autumn": "2Б"
        },
        "images": [
            {"title": ""},
            {"title": ""}
        ]
    }
    
    Response: Status 201 Created
    {
        "beauty_title": "Что-то красивое",
        "title": "Перевал",
        "other_titles": "Скиталец",
        "connect": "_",
        "users_id": {
            "full_name": "Иванов Иван Иванович",
            "email": "example@yandex.ru",
            "phone": "+79000000000"
        },
        "coord_id": {
            "latitude": 24.56,
            "longitude": 34.22,
            "height": 2200
        },
        "level_id": {
            "winter": "1А",
            "spring": "2А",
            "summer": "3Б",
            "autumn": "2Б"
        },
        "images": [
            {
                "images": null,
                "title": ""
            },
            {
                "images": null,
                "title": ""
            }
        ],
        "status": "Новый"
    }

Изменение записи
    
    PUT: 127.0.0.1:8000/api/v1/submitData/update/86
    {        
        "beauty_title": "Что-то красивое",
        "title": "Перевал",
        "other_titles": "Скиталец",
        "connect": "_",        
        "coord_id": {
            "latitude": 66.56,
            "longitude": 66.22,
            "height": 1000
        },
        "level_id": {
            "winter": "3Б",
            "spring": "1Б",
            "summer": "3А",
            "autumn": "3Б"
        },
        "images": [
            {
                "images": null,
                "title": "Название рисунка5"
            },
            {
                "images": null,
                "title": "Название рисунка6"
            }
        ]        
    }

    Response: Status 200 OK, (так как у записи статус "В работе")
    {
        "state": 0,
        "message": "Изменение невозможно. Информация на проверке модератора или принята"
    }

Просмотр

    GET: 127.0.0.1:8000/api/v1/submitData/86
    Response: Status 200 OK
    {
        "id": 86,
        "beauty_title": "Что-то красивое",
        "title": "Перевал",
        "other_titles": "Скиталец",
        "connect": "_",
        "users_id": {
            "full_name": "Иванов Иван Иванович",
            "email": "example@yandex.ru",
            "phone": "+79000000000"
        },
        "coord_id": {
            "latitude": 24.56,
            "longitude": 34.22,
            "height": 2200
        },
        "level_id": {
            "winter": "1А",
            "spring": "2А",
            "summer": "3Б",
            "autumn": "2Б"
        },
        "images": [
            {
                "images": null,
                "title": ""
            },
            {
                "images": null,
                "title": ""
            }
        ],
        "status": "В работе"
    }
