from django.shortcuts import render
from django.urls import reverse_lazy
from apps.organizations.models import Organization, Employee
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import OrganizationForm
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView


# Organization list view and update view

@login_required
def organization_list(request):

    search = request.GET.get("q", "")
    is_visible = request.GET.get("is_visible", "")

    organizations = Organization.objects.all().order_by("?")

    if is_visible == "":
        organizations = organizations.filter(is_visible=True)

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


# Employee list view and update view
@login_required
def employee_list(request):

    search = request.GET.get("q", "")
    is_active = request.GET.get("is_active", "")

    employees = Employee.objects.all().order_by('?')


    if is_active == "":
        employees = employees.filter(is_active=True)

    # Search filter
    if search:
        employees = employees.filter(
            Q(last_name__icontains=search) |
            Q(phone__icontains=search)
        )


    # Visibility filter
    if is_active == "true":
        employees = employees.filter(
            is_active=True
        )

    elif is_active == "false":
        employees = employees.filter(
            is_active=False
        )


    paginator = Paginator(employees, 12)

    page_obj = paginator.get_page(
        request.GET.get("page", 1)
    )


    context = {
        "employees": page_obj,
        "search": search,
        #"employees": employees,
        "is_htmx": request.headers.get("HX-Request"),
    }
    if request.headers.get("HX-Request"):
        return render(
            request,
            "organizations/employee/_cards.html",
            context
        )
    return render(
        request,
        "organizations/employee/list.html",
        context
    )