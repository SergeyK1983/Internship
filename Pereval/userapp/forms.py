from django import forms
from django.core.exceptions import ValidationError

"""
{
    "beauty_title": "Что-то красивое",
    "title": "Хибыны",
    "other_titles": "Скиталец",
    "connect": "_",
    "users_id": {
        "full_name": "Петров Иван Иванович",
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
            "title": "Фото1"
        },
        {
            "images": null,
            "title": "Фото2"
        }
    ]
}
"""


class CreateForm(forms.Form):
    LEVEL = [
        ("1А", "1А"), ("1Б", "1Б"), ("2А", "2А"), ("2Б", "2Б"), ("3А", "3А"), ("3Б", "3Б")
    ]

    beauty_title = forms.CharField(max_length=255)
    title = forms.CharField(max_length=255)
    other_titles = forms.CharField(max_length=255)
    connect = forms.CharField(max_length=255, initial='_')

    full_name = forms.CharField(max_length=255, initial="Петров Иван Иванович", label="ФИО")
    email = forms.EmailField(max_length=255, initial="example12@yandex.ru", label="Почта")
    phone = forms.CharField(max_length=11, initial='89110000000', label='Телефон', help_text='без пробелов')

    latitude = forms.FloatField(max_value=90.0, min_value=-90.0, label="Широта", help_text='в градусах')
    longitude = forms.FloatField(max_value=180.0, min_value=-180.0, label="Долгота", help_text='в градусах')
    height = forms.FloatField(max_value=8848.0, min_value=0.0, label="Высота", help_text='в метрах')

    winter = forms.ChoiceField(choices=LEVEL, initial=LEVEL[0], label="Зима")
    spring = forms.ChoiceField(choices=LEVEL, initial=LEVEL[0], label="Весна")
    summer = forms.ChoiceField(choices=LEVEL, initial=LEVEL[0], label="Лето")
    autumn = forms.ChoiceField(choices=LEVEL, initial=LEVEL[0], label="Осень")

    images = forms.ImageField(required=False)



