from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import APIException, NotFound
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PerevalAdded, Users
from .serializer import PerevalAddedSerializer, PerevalIDListSerializer, PerevalIDDetailSerializer, UsersSerializer, \
    PerevalUpdateModeratorSerializer, PerevalUpdateUsersSerializer


class PerevalIDList(generics.ListAPIView):
    """
    Контроллер GET-запроса на вывод id всех перевалов в БД
    """
    queryset = PerevalAdded.objects.all().values('id')
    serializer_class = PerevalIDListSerializer
    permission_classes = [permissions.AllowAny]


class PerevalUpdateModeratorAPI(generics.RetrieveUpdateAPIView):
    """
    Контроллер PUT-запроса на обновление статуса обработки поступившей информации о перевале
    """
    serializer_class = PerevalUpdateModeratorSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = PerevalAdded.objects.filter(pk=self.kwargs['pk'])
        return queryset


class PerevalRetrieveUpdateAPI(generics.RetrieveUpdateAPIView):
    """
    Контроллер PUT-запроса на изменение добавленной информации пока в статусе "Новое"
    """
    serializer_class = PerevalUpdateUsersSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = PerevalAdded.objects.filter(pk=self.kwargs['pk'])
        print(queryset[0].status)
        return queryset


class PerevalDetailAPI(APIView):
    """
    Контроллер GET-запроса на вывод информации о перевале по его id
    """
    serializer_class = PerevalIDDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        obj = get_object_or_404(PerevalAdded, pk=pk)
        return obj

    def get(self, request, pk, format=None):
        pereval = self.get_object(pk)
        serializer = PerevalIDDetailSerializer(pereval)
        return Response(serializer.data)


class PerevalEmailListAPI(generics.ListAPIView):
    """
    Контроллер GET-запроса на вывод информации о перевалах по email
    """
    serializer_class = PerevalIDDetailSerializer
    permission_classes = [permissions.AllowAny]
    # lookup_field = 'email'

    def get_queryset(self):
        try:
            user = Users.objects.get(email=self.kwargs['email'])
            queryset = user.pereval_user
            return queryset
        except ObjectDoesNotExist:
            pass

    def get(self, request, *args, **kwargs):
        if self.get_queryset() is None:
            data = {'error': 'Такого почтового адреса не зарегистрировано!', 'status': 'HTTP_404_NOT_FOUND'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        return self.list(request, *args, **kwargs)


class PerevalAddedCreate(generics.CreateAPIView):
    """
    Контроллер POST-запроса по форме клиента на создание новой записи в БД с информацией о перевале
    """
    serializer_class = PerevalAddedSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PerevalAddedSerializer(data=request.data)

        if not serializer.is_valid():
            data = {'error': 'Что-то пошло не так ...', 'status': 'HTTP_400_BAD_REQUEST'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():  # raise_exception=True
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except APIException:
                data = {'error': 'Сервер не отвечает.', 'status': 'HTTP_500_INTERNAL_SERVER_ERROR'}
                return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

