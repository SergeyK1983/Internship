from rest_framework import serializers
from .models import Users, PerevalAdded, Coords, DifficultyLevel, PerevalImages


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = (
            'full_name',
            'email',
            'phone',
        )


class PerevalAddedSerializer(serializers.ModelSerializer):

    class Meta:
        model = PerevalAdded
        fields = (
            'beautyTitle',
            'title',
            'other_titles',
        )
