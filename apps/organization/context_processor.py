import datetime
from .models import *

def organization_task_count(request):
    today = datetime.date.today()
    organization_total_task_count = Ergasies.objects.filter(importdate__year=today.year).count() or 0
    return { 'organization_total_task_count' : organization_total_task_count }
