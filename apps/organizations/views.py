from django.shortcuts import render


def organization_list(request):
    return render(request, "organizations/list.html")
