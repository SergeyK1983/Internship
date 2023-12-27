from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Users, PerevalAdded, Coords, DifficultyLevel, PerevalImages


class UsersSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100, label='Почта')

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
    winter = serializers.ChoiceField(choices=DifficultyLevel.Levels.labels, label='Зима')  # source='get_winter_display'
    spring = serializers.ChoiceField(choices=DifficultyLevel.Levels.labels, label='Весна')
    summer = serializers.ChoiceField(choices=DifficultyLevel.Levels.labels, label='Лето')
    autumn = serializers.ChoiceField(choices=DifficultyLevel.Levels.labels, label='Осень')

    class Meta:
        model = DifficultyLevel
        fields = (
            'winter',
            'spring',
            'summer',
            'autumn',
        )


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalImages
        fields = ['images', 'title']


class PerevalAddedSerializer(serializers.ModelSerializer):
    """
    Для создания записи в БД по форме от клиента
    """
    users_id = UsersSerializer(label='Отправитель')
    coord_id = CoordsSerializer(label='Координаты')
    level_id = DifficultyLevelSerializer(label='Уровень сложности')
    images = ImagesSerializer(label='Фотография', many=True)

    class Meta:
        model = PerevalAdded
        fields = (
            'beauty_title',
            'title',
            'other_titles',
            'connect',
            'users_id',
            'coord_id',
            'level_id',
            'images',  # по related_name
            'status',
        )
        read_only_fields = ('status', )
        extra_kwargs = {
            'status': {'choices': PerevalAdded.Status.labels, },
        }

    def create(self, validated_data):
        v_data = validated_data
        ordered_dict_users = v_data['users_id']
        ordered_dict_coord = v_data['coord_id']
        ordered_dict_level = v_data['level_id']
        ordered_dict_images = v_data.pop('images')

        def users_create(ordered_dict):
            if Users.objects.filter(email=ordered_dict['email']).exists():
                return Users.objects.get(email=ordered_dict['email'])
            users = Users(**ordered_dict)
            users.save()
            return users

        def coord_create(ordered_dict):
            coord = Coords(**ordered_dict)
            coord.save()
            return coord

        def level_create(ordered_dict):
            level = DifficultyLevel(**ordered_dict)
            level.save()
            return level

        users_id = users_create(ordered_dict_users)
        coord_id = coord_create(ordered_dict_coord)
        level_id = level_create(ordered_dict_level)
        v_data.update({'coord_id': coord_id, 'level_id': level_id, 'users_id': users_id})

        perevaladded = PerevalAdded.objects.create(**v_data)

        for images_dict in ordered_dict_images:
            PerevalImages.objects.create(pereval_id=perevaladded, **images_dict)

        return perevaladded


class PerevalIDListSerializer(serializers.ModelSerializer):
    """
    Для вывода информации о перевале по его id
    """
    users_id = UsersSerializer(label='Отправитель')
    coord_id = CoordsSerializer(label='Координаты')
    level_id = DifficultyLevelSerializer(label='Уровень сложности')
    images = ImagesSerializer(label='Фотография', many=True)

    class Meta:
        model = PerevalAdded
        fields = (
            'id',
            'beauty_title',
            'title',
            'other_titles',
            'connect',
            'users_id',
            'coord_id',
            'level_id',
            'images',  # по related_name
            'status',
        )
