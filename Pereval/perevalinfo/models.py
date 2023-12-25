from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .services import post_media_directory_path


class Users(models.Model):
    """
    Пользователи отправившие данные о перевале
    """
    full_name = models.CharField(max_length=150, verbose_name="ФИО")
    email = models.EmailField(max_length=100, unique=True, verbose_name="Почта")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    def __str__(self):
        return f"{self.pk}: {self.full_name}"


class PerevalAdded(models.Model):
    """
    Добавленная информация о перевалах
    """
    class Status(models.TextChoices):
        # A .label property is added on values, to return the human-readable name.
        NEW = "NW", _("Новый")  # при добавлении по умолчанию
        PENDING = "PN", _("В работе")  # модератор взял в работу
        ACCEPTED = "AC", _("Принято")  # модерация прошла успешно
        REJECTED = "RJ", _("Не принято")  # модерация прошла, информация не принята

    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.CharField(max_length=1, default="")  # непонятное поле по заданию
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.NEW, verbose_name='Состояние')
    users_id = models.ForeignKey(to=Users, related_name='pereval_user', on_delete=models.CASCADE, verbose_name='Автор')
    coord_id = models.OneToOneField(to='Coords', related_name='pereval_coord', on_delete=models.CASCADE,
                                    verbose_name='Координаты')
    level_id = models.ForeignKey(to='DifficultyLevel', related_name='pereval_level', on_delete=models.CASCADE,
                                 verbose_name='Сложность')

    def __str__(self):
        return f"{self.pk}- {self.beauty_title}"


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
    class Levels(models.TextChoices):
        # A .label property is added on values, to return the human-readable name.
        LEVEL1 = "LV1", _("1А")
        LEVEL2 = "LV2", _("1Б")
        LEVEL3 = "LV3", _("2А")
        LEVEL4 = "LV4", _("2Б")
        LEVEL5 = "LV5", _("3А")
        LEVEL6 = "LV6", _("3Б")

    winter = models.CharField(max_length=3, choices=Levels.choices, default=Levels.LEVEL1, blank=True, null=True,
                              verbose_name="Зима")
    spring = models.CharField(max_length=3, choices=Levels.choices, default=Levels.LEVEL1, blank=True, null=True,
                              verbose_name="Весна")
    summer = models.CharField(max_length=3, choices=Levels.choices, default=Levels.LEVEL1, blank=True, null=True,
                              verbose_name="Лето")
    autumn = models.CharField(max_length=3, choices=Levels.choices, default=Levels.LEVEL1, blank=True, null=True,
                              verbose_name="Осень")

    # def is_upperclass(self):  # get_winter_display
    #     return self.winter in {self.Levels.LEVEL1, self.Levels.LEVEL2, self.Levels.LEVEL3, self.Levels.LEVEL4,
    #     self.Levels.LEVEL5, self.Levels.LEVEL6}

    def __str__(self):
        return f"сложность: {self.pk}"


class PerevalImages(models.Model):
    """
    Фотографии перевалов
    """
    images = models.ImageField(upload_to=post_media_directory_path, blank=True, null=True, verbose_name="Фото")
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name="Название")
    pereval_id = models.ForeignKey(to=PerevalAdded, related_name='images', on_delete=models.CASCADE,
                                   verbose_name='Фотографии')

    def __str__(self):
        return f"фото: {self.pk}"
