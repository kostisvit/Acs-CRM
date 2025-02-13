import datetime
from .models import *
from organization.models import Ergasies

def task_count(request):
    today = datetime.date.today()
    if request.user.is_authenticated:
        context= { 'organization_total_task_count':Ergasies.objects.filter(importdate__year=today.year,employee=request.user).count() or 0}
        return context
    else:
        return{}

def adeia_count(request):
    today = datetime.date.today()
    if request.user.is_authenticated:
        context= { 'adeia_total':Adeia.objects.filter(created__year=today.year,acs_employee=request.user).count() or 0}
        return context
    else:
        return{}

def training_count(request):
    today = datetime.date.today()
    if request.user.is_authenticated:
        context= { 'training_total':Training.objects.filter(importdate__year=today.year,acs_employee=request.user).count() or 0}
        return context
    else:
        return{}