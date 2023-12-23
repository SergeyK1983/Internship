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
    pereval = UsersSerializer(label='Отправитель', required=True, many=False)
    coord_id = CoordsSerializer(label='Координаты')
    level_id = DifficultyLevelSerializer(label='Уровень сложности')
    images = PerevalImagesSerializer(label='Фотография')
    # images = PerevalImagesSerializer(label='Фотография', many=True)
    # status = serializers.ChoiceField(choices=)

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
            'images',
            'status',
        )
        # extra_kwargs = {
        #     'images':
        # }

    def create(self, validated_data):
        v_data = validated_data

        ordered_dict_coord = v_data['coord_id']
        ordered_dict_level = v_data['level_id']
        ordered_dict_pereval = v_data.pop('pereval')
        ordered_dict_images = v_data.pop('images')

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

        coord_id = coord_create(ordered_dict_coord)
        level_id = level_create(ordered_dict_level)
        v_data.update({'coord_id': coord_id, 'level_id': level_id})

        perevaladded = PerevalAdded.objects.create(**v_data)
        pereval = PerevalAdded.objects.get(id=perevaladded.id)

        us = Users(pereval_id=pereval, **ordered_dict_pereval)
        us.save(force_insert=True)

        # Users.objects.manager.create(pereval_id=perevaladded, **ordered_dict_pereval)
        PerevalImages.objects.create(pereval_id=perevaladded, **ordered_dict_images)

        return perevaladded

