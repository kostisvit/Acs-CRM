from django.shortcuts import render
from apps.organizations.models import Organization

def organization_list(request):
    organizations = Organization.objects.all()
    context = {
        'organizations':organizations
    }
    return render(request, "organizations/list.html", context)
