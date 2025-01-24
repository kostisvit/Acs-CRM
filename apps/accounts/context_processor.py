import datetime
from .models import *
from organization.models import Ergasies

def task_count(request):
    today = datetime.date.today()
    task_count = Ergasies.objects.filter(importdate__year=today.year,employee=request.user).count() or 0
    return {'task_count': task_count}

def adeia_count(request):
    today = datetime.date.today()
    adeia_count = Adeia.objects.filter(created__year=today.year,acs_employee=request.user).count() or 0
    return {'adeia_count': adeia_count}

def training_count(request):
    today = datetime.date.today()
    total_training = Training.objects.filter(importdate__year=today.year,acs_employee=request.user).count() or 0
    return {'total_training': total_training}