from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient, APITestCase

from .views import PerevalDetailAPI
from .models import Users, PerevalAdded, Coords, DifficultyLevel, PerevalImages


class SetUpPerevalinfo(APITestCase):
    def setUp(self):
        Users.objects.create(full_name='Кузнецов Иван Сидорович', email='ivan@yandex.ru', phone='+79119008080')
        Coords.objects.create(latitude=22.1, longitude=45.6, height=1200)
        DifficultyLevel.objects.create(winter="1А", spring="1А", summer="1А", autumn="1А")
        PerevalAdded.objects.create(
            beauty_title='Горы',
            title='Красивые горы',
            other_titles='Каменюки',
            connect='q',
            users_id=Users.objects.get(pk=1),
            coord_id=Coords.objects.get(pk=1),
            level_id=DifficultyLevel.objects.get(pk=1)
        )
        PerevalImages.objects.create(images=None, title=None, pereval_id=PerevalAdded.objects.get(pk=1))


class TestPerevalin(SetUpPerevalinfo):
    def test_PerevalDetailAPI(self):
        """
        Проверка содержимого по id
        """
        factory = APIRequestFactory()
        view = PerevalDetailAPI.as_view()
        # url = reverse('pereval-info')
        # response = self.client.get(url, format='json')
        request = factory.get('v1/pereval/1/')
        response = view(request, pk='1')
        print(response.data)
        response.render()  # Cannot access `response.content` without this.
        self.assertEquals(response.status_code, status.HTTP_200_OK)


class TestPerevalinf(APITestCase):
    def test_PerevalIDList(self):
        """
        Проверка вывода id перевалов
        """
        url = reverse('perevals')
        response = self.client.get(url, format='json')
        print(response.data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
