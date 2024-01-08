from django.urls import path, re_path
from .views import PerevalAddedCreate, PerevalDetailAPI, PerevalIDList, PerevalEmailListAPI, PerevalUpdateModeratorAPI, \
    PerevalRetrieveUpdateAPI

urlpatterns = [
    path('v1/create/', PerevalAddedCreate.as_view(), name='pereval-create'),
    path('v1/submitData/<int:pk>', PerevalDetailAPI.as_view(), name='pereval-info'),
    re_path(r'^v1/update/(?P<pk>[0-9]+)/$', PerevalUpdateModeratorAPI.as_view(), name='update-mod'),
    re_path(r'^v1/submitData/update/(?P<pk>[0-9]+)/$', PerevalRetrieveUpdateAPI.as_view(), name='update-user'),
    path('v1/submitData/<str:email>/', PerevalEmailListAPI.as_view(), name='perevals-user-email'),  # ?user__email=
    path('v1/perevals/', PerevalIDList.as_view(), name='perevals'),
]

