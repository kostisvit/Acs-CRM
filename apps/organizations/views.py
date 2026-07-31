from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from apps.organizations.models import Employee, Organization, Task
from apps.parameters.models import JobType, OtsSoftware

from .forms import EmployeeForm, OrganizationForm

User = get_user_model()
# Organization list view and update view


@login_required
def organization_list(request):

    search = request.GET.get("q", "")
    is_active = request.GET.get("is_active", "")

    organizations = Organization.objects.all().order_by("?")

    if is_active == "":
        organizations = organizations.filter(is_active=True)

    # Search filter
    if search:
        organizations = organizations.filter(
            Q(org_name__icontains=search) |
            Q(org_city__icontains=search) |
            Q(org_phone__icontains=search)
        )

    # Visibility filter
    if is_active == "true":
        organizations = organizations.filter(
            is_active=True
        )

    elif is_active == "false":
        organizations = organizations.filter(
            is_active=False
        )

    paginator = Paginator(organizations, 12)

    page_obj = paginator.get_page(
        request.GET.get("page", 1)
    )

    context = {
        "organizations": page_obj,
        "search": search,
        "is_active": is_active,
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


class OrganizationUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "organizations/detail.html"
    success_url = reverse_lazy("organizations:organization_list")
    success_message = "Ο Οργανισμός ενημερώθηκε με επιτυχία."

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
            Q(lastname__icontains=search) |
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
        # "employees": employees,
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


class EmployeeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "organizations/employee/detail.html"
    success_url = reverse_lazy("organizations:employee_list")
    success_message = "Ο Οργανισμός ενημερώθηκε με επιτυχία."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Επεξεργασία Επαφής"
        return context

# Soft delete and restore for Organization & Employee


def soft_delete_organization(request, pk):
    obj = get_object_or_404(Organization, pk=pk)
    obj.is_active = not obj.is_active
    obj.save(update_fields=["is_active"])
    messages.success(
        request, f'Ο Οργανισμός "{obj.org_name}" απενεργοποιήθηκε.')
    return redirect("organizations:organization_list")


def restore_organization(request, pk):
    obj = get_object_or_404(Organization, pk=pk)
    obj.is_active = True
    obj.save(update_fields=["is_active"])
    messages.success(request, f'Ο Οργανισμός "{obj.org_name}" ενεργοποιήθηκε.')
    return redirect("organizations:organization_list")


def soft_delete_employee(request, pk):
    obj = get_object_or_404(Employee, pk=pk)
    obj.is_active = False
    obj.save(update_fields=["is_active"])
    messages.success(
        request, f'Ο/H υπάλληλος "{obj.lastname} {obj.firstname}" του Οργανισμού "{obj.organization}" έχει απενεργοποιηθεί.')
    return redirect("organizations:employee_list")


def restore_employee(request, pk):
    obj = get_object_or_404(Employee, pk=pk)
    obj.is_active = True
    obj.save(update_fields=["is_active"])
    messages.success(
        request, f'Ο/H υπάλληλος "{obj.lastname} {obj.firstname}" του Οργανισμού "{obj.organization}" έχει εργοποιηθεί.')
    return redirect("organizations:employee_list")


# Task List
def task_list(request):
    if request.method == "POST":
        mode = request.POST.get("view_mode")

        if mode in ["cards", "table"]:
            request.session["task_view"] = mode

    # Filters
    search = request.GET.get("q", "")
    organization_id = request.GET.get("organization", "")
    org_app_id = request.GET.get("org_app", "")
    job_type_id = request.GET.get("job_type_acs", "")
    acs_employee_id = request.GET.get("acs_employee", "")
    org_employee_id = request.GET.get("org_employee", "")
    ticketid = request.GET.get("ticketid", "")
    importdate = request.GET.get("importdate", "")

    tasks = Task.objects.all()

    if organization_id:
        tasks = tasks.filter(organization_id=organization_id)

    if org_app_id:
        tasks = tasks.filter(org_app_id=org_app_id)

    if job_type_id:
        tasks = tasks.filter(job_type_acs_id=job_type_id)

    if acs_employee_id:
        tasks = tasks.filter(acs_employee_id=acs_employee_id)

    if org_employee_id:
        tasks = tasks.filter(org_employee_id=org_employee_id)

    if ticketid:
        tasks = tasks.filter(ticketid__icontains=ticketid)

    if importdate:
        tasks = tasks.filter(importdate=importdate)

    # Search all text fields
    if search:
        tasks = tasks.filter(
            Q(task_info__icontains=search)
            | Q(task_note__icontains=search)
            | Q(ticketid__icontains=search)
        )

    tasks = tasks.order_by("-importdate")

    paginator = Paginator(tasks, 12)

    page_obj = paginator.get_page(
        request.GET.get("page", 1)
    )

    context = {
        "tasks": page_obj,
        "search": search,
        "query_string": request.GET.urlencode(),
        "organization_id": organization_id,
        "org_app_id": org_app_id,
        "job_type_id": job_type_id,
        "acs_employee_id": acs_employee_id,
        "org_employee_id": org_employee_id,
        "ticketid": ticketid,
        "importdate": importdate,

        "organizations": Organization.objects.all(),
        "org_apps": OtsSoftware.objects.all(),
        "job_types": JobType.objects.all(),
        "acs_employees": get_user_model().objects.filter(groups__name="employee"),
        "org_employees": Employee.objects.all(),

        "is_htmx": request.headers.get("HX-Request"),
    }

    if request.headers.get("HX-Request"):
        return render(
            request,
            "organizations/task/_cards.html",
            context
        )

    return render(
        request,
        "organizations/task/list.html",
        context
    )
