from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import json

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
            print(data)
            user_id = {'user_id': {
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

            data.update(user_id)
            data.update(coord_id)
            data.update(level_id)
            data_json = json.dumps(data)
            # files = [("files", file)]
            # redirect to a new URL:
            print(data_json)
            # headers = {'Content-Type': 'application/json'}
            # headers = {'Content-Type': 'multipart/form-data'}
            # requests.post('http://127.0.0.1:8000/api/employees/', json=data_json, headers=headers)
            # requests.post('http://127.0.0.1:8000/api/employees/',data=data,headers=headers, files=files)
            return HttpResponse('/thanks/')
    return render(request, template_name='userapp/create.html', context=data)



