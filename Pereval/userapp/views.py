from base64 import b64encode
from collections import OrderedDict

from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
import requests
import json
from io import BytesIO

from .forms import CreateForm


def user_create_pereval(request):
    form = CreateForm
    data = {'title': "Создание записи перевала", 'form': form}
    if request.method == "POST":
        form_a = CreateForm(request.POST, request.FILES)
        if form_a.is_valid():
            # data = request.POST.copy()
            data = form_a.cleaned_data
            # data.pop("csrfmiddlewaretoken")
            # print(data)
            users_id = {'users_id': {
                "full_name": data.pop("full_name"),
                "email": data.pop("email"),
                "phone": data.pop("phone")
            }}
            coord_id = {'coord_id': {
                "latitude": data.pop("latitude"),
                "longitude": data.pop("longitude"),
                "height": data.pop("height")
            }}
            level_id = {'level_id': {
                "winter": data.pop("winter"),
                "spring": data.pop("spring"),
                "summer": data.pop("summer"),
                "autumn": data.pop("autumn")
            }}
            # img_data = OrderedDict(images=data.pop("images"), title="Фото 1")
            # print(img_data, type(img_data))

            data.update(users_id)
            data.update(coord_id)
            data.update(level_id)
            img = data.pop("images")
            d_vrem = {"images": [
                    # {"images": b64encode(img.read()).decode('utf-8'), "title": "Фото 1"},
                    {"images": img.read().decode('utf-8'), "title": "Фото 1"},
                    {"title": ""}
            ]}
            data.update(d_vrem)
            print(data)
            # print(data["images"], type(data["images"]))

            bytes_io = BytesIO()
            # print(img.content_type)
            # print(img.content_type_extra)
            # print(img.size)  # в байтах
            # print(img.name)
            # file = img(bytes_io, None, img.name, 'image/jpeg', bytes_io.getbuffer().nbytes, None)
            # files = [("images", open(img, 'rb'))]
            # files = b64encode(img.read()).decode('utf-8')

            data_json = json.dumps(data)
            # files = [("files", file)]
            # redirect to a new URL:
            print(data_json, type(data_json))
            headers = {'Content-Type': 'application/json'}
            # headers = {'Content-Type': 'multipart/form-data'}
            r = requests.post('http://127.0.0.1:8000/api/v1/create/', data=data_json, headers=headers, timeout=2)
            # r = requests.post(url='http://127.0.0.1:8000/api/v1/create/', json=data, headers=headers, files=files, timeout=2)
            print(r.text)
            print(r.json)
            # return HttpResponse('/thanks/')
            return JsonResponse(data)
    return render(request, template_name='userapp/create.html', context=data)



