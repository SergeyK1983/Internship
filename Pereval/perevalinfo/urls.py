from django.urls import path

from .views import PerevalAddedCreate, PerevalIDList, PerevalList

urlpatterns = [
    path('v1/create/', PerevalAddedCreate.as_view(), name='pereval-create'),
    path('v1/pereval/<int:pk>/', PerevalIDList.as_view(), name='pereval-info'),
    path('v1/perevals/', PerevalList.as_view(), name='perevals'),
]

