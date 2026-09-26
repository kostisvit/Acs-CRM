import os
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from apps.organizations.filters import ErgasiaFilter
from apps.organizations.models import Employee, Organization, Task
from apps.parameters.models import OrgDepartment

from .forms import EmployeeForm, OrganizationForm, TaskForm

User = get_user_model()


# Organization list view and update view
@login_required
def organization_list(request):

    search = request.GET.get("q", "")
    organization_id = request.GET.get("organization", "")
    is_active = request.GET.get("is_active", "")

    organizations = Organization.objects.all()

    # Active filter
    if is_active == "true":
        organizations = organizations.filter(is_active=True)
    elif is_active == "false":
        organizations = organizations.filter(is_active=False)
    else:
        organizations = organizations.filter(is_active=True)

    # Search filter
    if search:
        organizations = organizations.filter(
            Q(org_name__icontains=search)
            | Q(org_city__icontains=search)
            | Q(org_phone__icontains=search)
        )

    # Organization filter
    if organization_id:
        organizations = organizations.filter(id=organization_id)

    organizations = organizations.order_by("org_name")

    paginator = Paginator(organizations, 12)

    page_obj = paginator.get_page(request.GET.get("page", 1))

    context = {
        "organizations": page_obj,
        "search": search,
        "is_active": is_active,
        "organization_id": organization_id,
        "is_htmx": request.headers.get("HX-Request"),
    }

    if request.headers.get("HX-Request"):
        return render(request, "organizations/_cards.html", context)

    return render(request, "organizations/list.html", context)


class OrganizationCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "organizations/create.html"
    success_url = reverse_lazy("organizations:organization_list")
    success_message = "Ο Οργανισμός δημιουργήθηκε με επιτυχία."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Δημιουργία Πελάτη"
        return context

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     # Additional logic after saving the form can be added here
    #     return response


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


# Employee list view and update view & create view
@login_required
def employee_list(request):

    search = request.GET.get("q", "")
    organization_id = request.GET.get("organization", "")
    department_id = request.GET.get("org_department", "")
    is_active = request.GET.get("is_active", "")

    employees = Employee.objects.all()

    # Organization filter
    if organization_id:
        employees = employees.filter(organization_id=organization_id)

    # Department filter
    if department_id:
        employees = employees.filter(org_department_id=department_id)

    # Active filter
    if is_active == "true":
        employees = employees.filter(is_active=True)

    elif is_active == "false":
        employees = employees.filter(is_active=False)

    else:
        employees = employees.filter(is_active=True)

    # Search filter
    if search:
        employees = employees.filter(
            Q(firstname__icontains=search)
            | Q(lastname__icontains=search)
            | Q(phone__icontains=search)
            | Q(mobile__icontains=search)
            | Q(email__icontains=search)
        )

    employees = employees.order_by("lastname", "firstname")

    paginator = Paginator(employees, 12)

    page_obj = paginator.get_page(request.GET.get("page", 1))

    context = {
        "employees": page_obj,
        # Current filters
        "search": search,
        "organization_id": organization_id,
        "department_id": department_id,
        "is_active": is_active,
        # Filter dropdowns
        "organizations": Organization.objects.filter(is_active=True),
        "departments": OrgDepartment.objects.all(),
        "is_htmx": request.headers.get("HX-Request"),
    }

    if request.headers.get("HX-Request"):
        return render(request, "organizations/employee/_cards.html", context)

    return render(request, "organizations/employee/list.html", context)


class EmployeeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "organizations/employee/create.html"
    success_url = reverse_lazy("organizations:employee_list")
    success_message = "Η επαφή δημιουργήθηκε με επιτυχία."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Δημιουργία Επαφής"
        return context

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     return response


class EmployeeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "organizations/employee/detail.html"
    success_url = reverse_lazy("organizations:employee_list")
    success_message = "Η επαφή ενημερώθηκε με επιτυχία."

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
        request,
        f'Ο/H υπάλληλος "{obj.lastname} {obj.firstname}" του Οργανισμού "{obj.organization}" έχει απενεργοποιηθεί.',
    )
    return redirect("organizations:employee_list")


def restore_employee(request, pk):
    obj = get_object_or_404(Employee, pk=pk)
    obj.is_active = True
    obj.save(update_fields=["is_active"])
    messages.success(
        request,
        f'Ο/H υπάλληλος "{obj.lastname} {obj.firstname}" του Οργανισμού "{obj.organization}" έχει εργοποιηθεί.',
    )
    return redirect("organizations:employee_list")


# Task List
@login_required
def task_list(request):
    if request.method == "POST":
        mode = request.POST.get("view_mode")

        if mode in ["cards", "table"]:
            request.session["task_view"] = mode

    queryset = (
        Task.objects
        .select_related(
            "organization",
            "org_app",
            "job_type_acs",
            "acs_employee",
            "org_employee",
        )
        .order_by("-importdate", "-pk")
    )

    task_filter = ErgasiaFilter(
        request.GET,
        queryset=queryset,
    )

    # All records / filtered records
    tasks = task_filter.qs

    # Check whether at least one actual filter was selected
    has_filters = any(
        value.strip()
        for key, value in request.GET.items()
        if key != "page" and value.strip()
    )

    if has_filters:
        task_count_by_organization = tasks.count()

        task_time_by_organization = (
            tasks.aggregate(
                total=Sum("task_time")
            )["total"] or Decimal("0")
        )
    else:
        task_count_by_organization = 0
        task_time_by_organization = Decimal("0")

    paginator = Paginator(tasks, 12)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop("page", None)

    query_string = query_params.urlencode()
    context = {
        "filter": task_filter,
        "tasks": page_obj,
        "page_obj": page_obj,
        "query_string": query_string,
        "task_count_by_organization": task_count_by_organization,
         "task_time_by_organization": task_time_by_organization,
        "is_htmx": request.headers.get("HX-Request"),
    }

    if request.headers.get("HX-Request"):

        # "Περισσότερα"
        if request.GET.get("page"):
            return render(
                request,
                "organizations/task/_task_load_more_response.html",
                context,
            )

        # Filter / search
        return render(
            request,
            "organizations/task/_task_results.html",
            context,
        )

    return render(
        request,
        "organizations/task/list.html",
        context,
    )


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "organizations/task/create.html"
    success_url = reverse_lazy("organizations:task_list")
    success_message = "Η εργασία δημιουργήθηκε με επιτυχία."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Δημιουργία Εργασίας"
        return context

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     return response


class TaskListUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "organizations/task/detail.html"
    success_url = reverse_lazy("organizations:task_list")
    success_message = "Η εργασία ενημερώθηκε με επιτυχία."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Επεξεργασία Εργασίας"
        return context


def load_employees(request):
    organization_id = request.GET.get("organization_id")

    employees = Employee.objects.filter(
        organization_id=organization_id
    ).values("id", "lastname", "firstname").order_by("lastname", "firstname")

    return JsonResponse(list(employees), safe=False)


def download_skipped_rows(request):
    file_path = request.session.get("skipped_file_path")
    if file_path and os.path.exists(file_path):
        return FileResponse(open(file_path, "rb"), as_attachment=True, filename="skipped_rows.xlsx")
    messages.error(request, "No skipped rows file available.")
    return redirect("import_task")
