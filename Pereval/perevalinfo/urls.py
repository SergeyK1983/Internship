from django.urls import path

from .views import PerevalAddedCreate, PerevalDetailListAPI, PerevalIDList, PerevalEmailListAPI

urlpatterns = [
    path('v1/create/', PerevalAddedCreate.as_view(), name='pereval-create'),
    path('v1/pereval/<int:pk>/', PerevalDetailListAPI.as_view(), name='pereval-info'),
    path('v1/submitData/<str:email>/', PerevalEmailListAPI.as_view(), name='pereval-info'),  # ?user__email=
    path('v1/perevals/', PerevalIDList.as_view(), name='perevals'),
]

# url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
# from django.conf.urls import url