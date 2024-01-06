from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Users, PerevalAdded, Coords, DifficultyLevel, PerevalImages


class SetUpPerevalinfo(APITestCase):
    def setUp(self):
        """ Исходные данные """
        self.some_user = Users.objects.create(full_name='Кузнецов Иван Сидорович', email='ivan@yandex.ru',
                                              phone='+79119008080')
        self.some_coord = Coords.objects.create(latitude=22.1, longitude=45.6, height=1200)
        self.some_coord_em = Coords.objects.create(latitude=67.64, longitude=33.59, height=1067)
        self.some_level = DifficultyLevel.objects.create(winter="1А", spring="1А", summer="1А", autumn="1А")
        self.some_level_em = DifficultyLevel.objects.create(winter="2А", spring="3Б", summer="3А", autumn="2А")
        self.some_pereval = PerevalAdded.objects.create(
            beauty_title='Горы',
            title='Красивые горы',
            other_titles='Каменюки',
            connect='q',
            users_id=self.some_user,  # self.some_user.id (Err. must be a "Users" instance)
            coord_id=self.some_coord,  # Coords.objects.get(pk=1), так тоже возникают ошибки, но при прохождении тестов
            level_id=self.some_level
        )
        self.some_pereval_em = PerevalAdded.objects.create(
            beauty_title='Красота севера',
            title='Хибины',
            other_titles='Сопки',
            connect='_',
            users_id=self.some_user,
            coord_id=self.some_coord_em,
            level_id=self.some_level_em
        )
        self.some_image = PerevalImages.objects.create(images=None, title=None, pereval_id=self.some_pereval)
        self.some_image_em = PerevalImages.objects.create(images=None, title="Фото 1", pereval_id=self.some_pereval_em)
        self.some_image_em = PerevalImages.objects.create(images=None, title="Фото 2", pereval_id=self.some_pereval_em)

        self.some_data = {
            'id': self.some_pereval.id,
            'beauty_title': 'Горы',
            'title': 'Красивые горы',
            'other_titles': 'Каменюки',
            'connect': 'q',
            'users_id': {'full_name': 'Кузнецов Иван Сидорович', 'email': 'ivan@yandex.ru', 'phone': '+79119008080'},
            'coord_id': {'latitude': 22.1, 'longitude': 45.6, 'height': 1200},
            'level_id': {'winter': '1А', 'spring': '1А', 'summer': '1А', 'autumn': '1А'},
            'images': [{'images': None, 'title': None}],
            'status': 'Новый'
        }

        self.one_post_data = {
            'beauty_title': 'Северный урал',
            'title': 'Урал',
            'other_titles': 'Уральские горы',
            'connect': '_',
            'users_id': {'full_name': 'Петров Степан Иванович', 'email': 'stepan@yandex.ru', 'phone': '+79539008000'},
            'coord_id': {'latitude': 64.1, 'longitude': 59.6, 'height': 1617},
            'level_id': {'winter': '2А', 'spring': '2А', 'summer': '2А', 'autumn': '2А'},
            'images': [{'images': None, 'title': 'фото1'}]
        }

        self.status_update_data = {
            'status': PerevalAdded.Status.PENDING.label
        }
        self.user_update_data = {
            'beauty_title': 'Зелёные холмы',
            'title': 'Высокогорье',
            'other_titles': 'Пристанище хоббитов',
            'connect': 'q',
            'coord_id': {'latitude': 22.1, 'longitude': 45.6, 'height': 1200},
            'level_id': {'winter': '3Б', 'spring': '3Б', 'summer': '3Б', 'autumn': '3Б'},
            'images': [{'images': None, 'title': None}]
        }

    def test_PerevalAddedCreate(self):
        """ Тест на создание записи в БД """
        url = reverse(viewname='pereval-create')
        response = self.client.post(url, data=self.one_post_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data['status'], PerevalAdded.Status.NEW.label)

    def test_fail_PerevalDetailAPI(self):
        """ Тест на обращение по несуществующему id перевала """
        url = reverse(viewname='pereval-info', kwargs={'pk': 86})
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_PerevalDetailAPI(self):
        """ Тест на обращение по id перевала """
        url = reverse(viewname='pereval-info', kwargs={'pk': self.some_pereval.id})
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 10)
        self.assertEquals(response.json(), self.some_data)

    def test_fail_PerevalEmailListAPI(self):
        """ Тест на обращение по несуществующему email пользователя """
        url = reverse(viewname='perevals-user-email', kwargs={'email': 'email@yandex.ru'})
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_PerevalEmailListAPI(self):
        """ Тест на обращение по email пользователя """
        url = reverse(viewname='perevals-user-email', kwargs={'email': self.some_user.email})
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 2)

    def test_PerevalIDList(self):
        """ Проверка вывода id перевалов """
        url = reverse('perevals')
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_PerevalRetrieveUpdateAPI(self):
        """ Тест на обновление записи в БД """
        url = reverse(viewname='update-user', kwargs={'pk': self.some_pereval.id})
        response = self.client.put(url, data=self.user_update_data, format='json')
        response_get = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response_get.data['status'], PerevalAdded.Status.NEW.label)

    def test_fail_PerevalRetrieveUpdateAPI(self):
        """ Тест на запрет обновления записи в БД """
        p = PerevalAdded.objects.get(pk=self.some_pereval.id)
        p.status = PerevalAdded.Status.PENDING.label
        p.save()
        url = reverse(viewname='update-user', kwargs={'pk': self.some_pereval.id})
        response = self.client.put(url, data=self.user_update_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['state'], 0)

    def test_PerevalUpdateModeratorAPI(self):
        """ Тест на обновление статуса записи в БД """
        url = reverse(viewname='update-mod', kwargs={'pk': self.some_pereval_em.id})
        response = self.client.put(url, data=self.status_update_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['status'], PerevalAdded.Status.PENDING.label)

    def test_count_users(self):
        count = Users.objects.all().count()
        self.assertEquals(count, 1)
