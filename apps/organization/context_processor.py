import datetime
from .models import *

def organization_task_count(request,custom_user=None):
    today = datetime.date.today()
    if request.user.is_authenticated:
        user = custom_user or request.user
        organization_total_task_count = Ergasies.objects.filter(importdate__year=today.year,employee=user).count() or 0
        return { 'organization_total_task_count' : organization_total_task_count }
    else:
        return {}
