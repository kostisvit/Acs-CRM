from apps.organizations.models import Organization, Employee

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