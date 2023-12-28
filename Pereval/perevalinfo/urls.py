from django.urls import path, re_path
from .views import PerevalAddedCreate, PerevalDetailAPI, PerevalIDList, PerevalEmailListAPI, PerevalUpdateModeratorAPI

urlpatterns = [
    path('v1/create/', PerevalAddedCreate.as_view(), name='pereval-create'),
    re_path(r'^v1/pereval/(?P<pk>[0-9]+)/$', PerevalDetailAPI.as_view(), name='pereval-info'),
    re_path(r'^v1/update/(?P<pk>[0-9]+)/$', PerevalUpdateModeratorAPI.as_view(), name='update-mod'),
    path('v1/submitData/<str:email>/', PerevalEmailListAPI.as_view(), name='pereval-info'),  # ?user__email=
    path('v1/perevals/', PerevalIDList.as_view(), name='perevals'),
]

