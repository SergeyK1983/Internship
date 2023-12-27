from rest_framework.exceptions import APIException
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializer import PerevalAddedSerializer


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

