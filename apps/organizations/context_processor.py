import datetime

from django.db.models import Sum

from apps.organizations.models import Employee, Organization, Task

# Custom context processor for organization, contacts, tasks


def organization_count(request):
    if request.user.is_authenticated:
        return {"total_organization": Organization.objects.filter(is_active=True).count()}
    total_organization = 0
    return {'total_organization': total_organization}


def org_employees_count(request):
    if request.user.is_authenticated:
        return {'total_employees': Employee.objects.filter(is_active=True).count()}
    total_employees = 0
    return {'total_employees': total_employees}


def org_tasks_count(request):
    today = datetime.datetime.now(tz=datetime.UTC).date()
    if request.user.is_authenticated:
        return {'total_tasks': Task.objects.filter(importdate__year=today.year).count()}
    total_tasks = 0
    return {'total_tasks': total_tasks}

def user_work_time(request):
    if not request.user.is_authenticated:
        return {}

    today = datetime.datetime.now(tz=datetime.UTC).date()

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
