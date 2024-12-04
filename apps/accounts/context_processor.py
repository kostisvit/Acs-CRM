import datetime
from .models import *


def adeia_count(request):
    today = datetime.date.today()
    adeia_count = Adeia.objects.filter(created__year=today.year).count() or 0
    return {'adeia_count': adeia_count}

def training_count(request):
    today = datetime.date.today()
    total_training = Training.objects.filter(importdate__year=today.year).count() or 0
    return {'total_training': total_training}