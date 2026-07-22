
import csv
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from openpyxl import Workbook
from apps.organizations.models import Organization
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import CSVUploadForm, OrganizationForm
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView

@login_required
def organization_list(request):

    search = request.GET.get("q", "")
    is_visible = request.GET.get("is_visible", "")

    organizations = Organization.objects.all().order_by("org_name")


    # Search filter
    if search:
        organizations = organizations.filter(
            Q(org_name__icontains=search) |
            Q(org_city__icontains=search) |
            Q(org_phone__icontains=search)
        )


    # Visibility filter
    if is_visible == "true":
        organizations = organizations.filter(
            is_visible=True
        )

    elif is_visible == "false":
        organizations = organizations.filter(
            is_visible=False
        )


    paginator = Paginator(organizations, 12)

    page_obj = paginator.get_page(
        request.GET.get("page", 1)
    )


    context = {
        "organizations": page_obj,
        "search": search,
        "is_visible": is_visible,
        "is_htmx": request.headers.get("HX-Request"),
    }
    if request.headers.get("HX-Request"):
        return render(
            request,
            "organizations/_cards.html",
            context
        )
    return render(
        request,
        "organizations/list.html",
        context
    )




class OrganizationUpdateView(SuccessMessageMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "organizations/detail.html"
    success_url = reverse_lazy("organizations:organization_list")
    success_message = "Ο πελάτης ενημερώθηκε επιτυχώς."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Επεξεργασία Πελάτη"
        return context