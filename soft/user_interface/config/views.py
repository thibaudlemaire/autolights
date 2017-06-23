from django.shortcuts import render, get_object_or_404
from datetime import datetime
from config.models import Configuration


call_function = None


def set_call_function(function):
    global call_function
    call_function = function


def list_config(request):
    date = datetime.now()
    configs = Configuration.objects.all()
    return render(request, 'config/list-config.html', locals())


def edit_config(request, id):
    get_object_or_404(Configuration, id=id)
    return render(request, 'config/edit-config.html', locals())


def home(request):
    return render(request, 'config/home.html')