from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from .services import post_media_directory_path


class Users(models.Model):
    """
    Пользователи отправившие данные о перевале
    """
    full_name = models.CharField(max_length=150, verbose_name="ФИО")
    email = models.EmailField(max_length=100, unique=True, verbose_name="Почта")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    pereval_id = models.ForeignKey(to='PerevalAdded', related_name='pereval', on_delete=models.CASCADE,
                                   verbose_name='Доб. перевалы')

    def __str__(self):
        return f"{self.pk}: {self.full_name}"


class PerevalAdded(models.Model):
    """
    Добавленная информация о перевалах
    """
    NEW = 'NE'  # при добавлении по умолчанию
    PENDING = 'PE'  # модератор взял в работу
    ACCEPTED = 'AC'  # модерация прошла успешно
    REJECTED = 'RE'  # модерация прошла, информация не принята

    STATUS = [
        (NEW, 'Новый'),
        (PENDING, 'В работе'),
        (ACCEPTED, 'Принято'),
        (REJECTED, 'Не принято'),
    ]

    beautyTitle = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.CharField(max_length=1, default=" ")  # непонятное поле по заданию
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    status = models.CharField(max_length=2, choices=STATUS, default=NEW, verbose_name='Состояние')
    coord_id = models.ForeignKey(to='Coords', related_name='coord', on_delete=models.CASCADE, verbose_name='Координаты')
    level_id = models.ForeignKey(to='DifficultyLevel', related_name='level', on_delete=models.CASCADE,
                                 verbose_name='Сложность')

    def __str__(self):
        return f"{self.pk}- {self.beautyTitle}"


class Coords(models.Model):
    """
    Координаты перевала
    """
    latitude = models.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)], default=34.3,
                                 verbose_name="Широта", help_text="широта в градусах")
    longitude = models.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)], default=61.8,
                                  verbose_name="Долгота", help_text="долгота в градусах")
    height = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(8848)], default=0,
                                 verbose_name="Высота", help_text="высота в метрах над уровнем моря")

    def __str__(self):
        return f"широта: {self.latitude}, долгота: {self.longitude}"


class DifficultyLevel(models.Model):
    """
    Уровни сложности в разное время года
    """
    winter = models.CharField(max_length=10, blank=True, null=True, verbose_name="Зима")
    spring = models.CharField(max_length=10, blank=True, null=True, verbose_name="Весна")
    summer = models.CharField(max_length=10, blank=True, null=True, verbose_name="Лето")
    autumn = models.CharField(max_length=10, blank=True, null=True, verbose_name="Осень")

    def __str__(self):
        return f"сложность: {self.pk}"


class PerevalImages(models.Model):
    """
    Фотографии перевалов
    """
    images = models.ImageField(upload_to=post_media_directory_path, blank=True, null=True, verbose_name="Фото")
    pereval_id = models.ForeignKey(to=PerevalAdded, related_name='images', on_delete=models.CASCADE,
                                  verbose_name='Фотографии')

    def __str__(self):
        return f"фото: {self.pk}"

