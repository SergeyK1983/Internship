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
            # 'pereval_id'
        )
        # read_only_fields = ('pereval_id', )


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
    """
    Для создания записи в БД по форме от клиента
    """
    users_id = UsersSerializer(label='Отправитель')
    coord_id = CoordsSerializer(label='Координаты')
    level_id = DifficultyLevelSerializer(label='Уровень сложности')
    images = PerevalImagesSerializer(label='Фотография')
    # images = PerevalImagesSerializer(label='Фотография', many=True)
    # status = serializers.ChoiceField(choices=)

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
        # extra_kwargs = {
        #     'beauty_title': {'initial': "Горы"}
        # }

    def create(self, validated_data):
        v_data = validated_data
        print(v_data)

        ordered_dict_users = v_data['users_id']
        ordered_dict_coord = v_data['coord_id']
        ordered_dict_level = v_data['level_id']
        ordered_dict_images = v_data.pop('images')

        def users_create(ordered_dict):
            print(ordered_dict)
            users = Users(**ordered_dict)
            users.save()
            instance = Users.objects.all().last()
            return instance

        def coord_create(ordered_dict):
            coord = Coords(**ordered_dict)
            coord.save()
            instance = Coords.objects.all().last()
            return instance

        def level_create(ordered_dict):
            level = DifficultyLevel(**ordered_dict)
            level.save()
            instance = DifficultyLevel.objects.all().last()
            return instance

        users_id = users_create(ordered_dict_users)
        coord_id = coord_create(ordered_dict_coord)
        level_id = level_create(ordered_dict_level)
        v_data.update({'coord_id': coord_id, 'level_id': level_id, 'users_id': users_id})

        perevaladded = PerevalAdded.objects.create(**v_data)
        pereval = PerevalAdded.objects.get(id=perevaladded.id)

        # us = Users(pereval_id=pereval, **ordered_dict_pereval)
        # us.save(force_insert=True)

        # Users.objects.manager.create(pereval_id=perevaladded, **ordered_dict_pereval)
        PerevalImages.objects.create(pereval_id=perevaladded, **ordered_dict_images)

        return perevaladded

