from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Users, PerevalAdded, Coords, DifficultyLevel, PerevalImages


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            'full_name',
            'email',
            'phone',
        )


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = (
            'latitude',
            'longitude',
            'height',
        )


class DifficultyLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DifficultyLevel
        fields = (
            'winter',
            'spring',
            'summer',
            'autumn',
        )


class PerevalImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalImages
        fields = (
            'images',
        )


class PerevalAddedSerializer(serializers.ModelSerializer):
    pereval = UsersSerializer(label='Отправитель')
    coord_id = CoordsSerializer(label='Координаты')
    level_id = DifficultyLevelSerializer(label='Уровень сложности')
    images1 = PerevalImagesSerializer(label='Фотография 1')
    images2 = PerevalImagesSerializer(label='Фотография 2')
    images3 = PerevalImagesSerializer(label='Фотография 3')

    class Meta:
        model = PerevalAdded
        fields = (
            'beautyTitle',
            'title',
            'other_titles',
            'connect',
            'pereval',  # по related_name='pereval'
            'coord_id',
            'level_id',
            'images1',
            'images2',
            'images3',
        )

