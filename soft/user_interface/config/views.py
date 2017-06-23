from django.shortcuts import render, get_object_or_404
from datetime import datetime
from config.models import *


def list_config(request):
    date = datetime.now()
    configs = Configuration.objects.all()
    return render(request, 'config/list-config.html', locals())


def edit_config(request, id):
    config = get_object_or_404(Configuration, id=id)
    continuous_rules = ContinuousRule.objects.all()
    return render(request, 'config/edit-config.html', locals())


def home(request):
    return render(request, 'config/home.html')


def add_config(request):
    config = Configuration()
    config.save()
    return render(request, 'config/edit-config.html', locals())


def edit_continuous_rule(request):
    return render(request, 'config/edit-continuous-rule.html', locals())