import datetime
from django.db.models import Sum
from apps.organizations.models import Organization, Employee, Task

# Custom context processor for organization, contacts, tasks and day off count


def organization_count(request):
    if request.user.is_authenticated:
        return {"total_organization": Organization.objects.filter(is_active=True).count()}
    else:
        return {}


def org_employees_count(request):
    if request.user.is_authenticated:
        return {'total_employees': Employee.objects.filter(is_active=True).count()}
    else:
        return {}


def org_tasks_count(request):
    today = datetime.date.today()
    if request.user.is_authenticated:
        return {'total_tasks': Task.objects.filter(importdate__year=today.year).count()}
    else:
        return {}


def user_work_time(request):
    if not request.user.is_authenticated:
        return {}

    today = datetime.date.today()

    user_work_time = 0
    user_work_count = 0
    last_record = None

    groups = request.user.groups.values_list("name", flat=True)

    if "manager" in groups:
        queryset = Task.objects.filter(
            importdate__year=today.year
        )

    elif "employee" in groups:
        queryset = Task.objects.filter(
            acs_employee=request.user,
            importdate__year=today.year
        )

    else:
        queryset = Task.objects.none()

    user_work_time = queryset.aggregate(
        total=Sum("task_time")
    )["total"] or 0

    user_work_count = queryset.count()

    last_record = queryset.order_by(
        "-importdate",
        "-id"
    ).first()

    return {
        "user_work_time": user_work_time,
        "last_record": last_record,
        "user_work_count": user_work_count,
    }
