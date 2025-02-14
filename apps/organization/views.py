from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django_filters.views import FilterView
from .models import Organization, Employee, Ergasies, Application
from .filters import OrganizationFilter, OrgEmpoloyeeFilter, TaskFilter
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
import json
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import OrganizationForm,ApplicationForm,OrgEmployeeForm
from .export import export_organization_data
from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.core.paginator import Paginator
from .forms import TaskForm
from django.core import serializers
from .delete_view import *



##################################################################################

#Λίστα πελατών
@login_required
def organization_list(request):
    # Step 1: Get the filtered queryset
    organization_list = Organization.objects.visible()
    organization_filter = OrganizationFilter(request.GET, queryset=organization_list)

    # Step 2: Apply pagination
    paginator = Paginator(organization_filter.qs, 10)  # 10 tasks per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)

    # Step 3: Get filter query params
    filter_params = request.GET.copy()  # Copy request.GET to preserve existing filters
    if filter_params.get('page'):
        filter_params.pop('page')

    form = OrganizationForm()  # Default form (used in GET requests)
    show_modal = False  # Default flag for modal visibility

    if request.method == "POST":
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})  # Redirect to a success page after saving
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = OrganizationForm()  # Show modal if the form is invalid

    # Step 4: Render the template with context
    context = {
        'page_obj': page_obj,
        'filter': organization_filter,
        'filter_params': filter_params.urlencode(),
        'form': form,  # Pass the form (valid or with errors)
        'show_modal': show_modal,  # Pass modal visibility flag
    }

    return render(request, 'apps/organization/organization_list.html', context)


class OrganizationListViewVisibleFalse(LoginRequiredMixin,FilterView):
    model = Organization
    context_object_name = 'foreas_list'
    template_name = 'apps/organization/organization_inactive.html'
    filterset_class = OrganizationFilter
    ordering = ['name']
    paginate_by = 10  

    def get_queryset(self):
        """
        Use the custom manager to filter inactive records (is_visible=False).
        """
        return Organization.objects.invisible()

#Διόρθωση εγγραφών πελατών
@login_required
def edit_organization(request, organization_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        organization = get_object_or_404(Organization, id=organization_id)
        organization.name = data.get('name')
        organization.address = data.get('address')
        organization.city = data.get('city')
        organization.phone = data.get('phone')
        organization.email = data.get('email')
        organization.website = data.get('website')
        organization.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed'}, status=400)

@login_required
def soft_delete_organization(request, pk):
    """Soft delete"""
    organization = get_object_or_404(Organization, pk=pk)
    organization.delete()
    return redirect('organization_list')
    
@login_required
def restore_organization(request, pk):
    """Restore a soft-deleted product."""
    organization = get_object_or_404(Organization, pk=pk)
    organization.restore()
    return redirect('organization_list')

##################################################################################

#Λίστα Επαφών Οργανισμού

@login_required
def org_employee_list(request):
    # Step 1: Get the filtered queryset
    org_employee_list = Employee.objects.visible()
    org_employee_filter = OrgEmpoloyeeFilter(request.GET, queryset=org_employee_list)

    # Step 2: Apply pagination
    paginator = Paginator(org_employee_filter.qs, 10)  # 10 tasks per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)

    # Step 3: Get filter query params
    filter_params = request.GET.copy()  # Copy request.GET to preserve existing filters
    if filter_params.get('page'):
        filter_params.pop('page')

    form = OrgEmployeeForm()  # Default form (used in GET requests)
    show_modal = False  # Default flag for modal visibility

    if request.method == "POST":
        form = OrgEmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})  # Redirect to a success page after saving
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = OrgEmployeeForm()  # Show modal if the form is invalid

    # Step 4: Render the template with context
    context = {
        'org_employee_list': page_obj,
        'filter': org_employee_filter,
        'filter_params': filter_params.urlencode(),
        'form': form,  # Pass the form (valid or with errors)
        'show_modal': show_modal,  # Pass modal visibility flag
    }

    return render(request, 'apps/organization/organization_contact.html', context)




#Διόρθωση εγγραφών πελατών
@login_required
def edit_contact(request, employee_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        employee = get_object_or_404(Employee, id=employee_id)
        employee.firstname = data.get('firstname')
        employee.lastname = data.get('lastname')
        employee.tmhma = data.get('tmhma')
        employee.phone = data.get('phone')
        employee.cellphone = data.get('cellphone')
        employee.email = data.get('email')
        employee.secondary_email = data.get('secondary_email')
        
        employee.is_visible = data.get('is_visible')
        employee.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed'}, status=400)


def soft_delete_contact(request, pk):
    """Soft delete"""
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect('org_employee')

def restore_contact(request, pk):
    """Restore a soft-deleted product."""
    employee = get_object_or_404(Employee, pk=pk)
    employee.restore()
    return redirect('org_employee')

##################################################################################

# Λίστα Εργασιών Οργανισμού

@login_required
def organization_tasks(request):
    today = datetime.date.today()

    # Step 1: Get the filtered queryset
    task_list = Ergasies.objects.filter(employee=request.user)
    task_filter = TaskFilter(request.GET, queryset=task_list)

    # Step 2: Apply pagination
    paginator = Paginator(task_filter.qs, 10)  # 9 tasks per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)

    # Step 3: Get filter query params
    filter_params = request.GET.copy()  # Copy request.GET to preserve existing filters
    if filter_params.get('page'):
        filter_params.pop('page')  # Remove 'page' parameter to prevent it from being included in the filter query
        
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = TaskForm()
    # Step 4: Render the template with context
    context = {
        'page_obj': page_obj,
        'filter': task_filter,
        'filter_params': filter_params.urlencode(),
        'form': form, # Pass the encoded filter query params
    }


    return render(request, 'apps/organization/organization_tasks.html', context)

@login_required
def edit_task(request, task_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        task = get_object_or_404(Ergasies, id=task_id)
        task.info = data.get('info')
        task.importdate =  data.get('importdate')
        # ergasies.lastname = data.get('lastname')
        # ergasies.tmhma = data.get('tmhma')
        # ergasies.phone = data.get('phone')
        # ergasies.cellphone = data.get('cellphone')
        # ergasies.email = data.get('email')
        # ergasies.secondary_email = data.get('secondary_email')
        
        # ergasies.is_visible = data.get('is_visible')
        task.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed'}, status=400)


def soft_delete_task(request, pk):
    """Soft delete"""
    task = get_object_or_404(Ergasies, pk=pk)
    task.delete()
    return redirect('tasks')

def restore_task(request, pk):
    """Restore a soft-deleted product."""
    task = get_object_or_404(Ergasies, pk=pk)
    task.restore()
    return redirect('tasks')

##################################################################################

# Λίστα εφαρνογών

@login_required
def application_view(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('application_view')  # Reload to display updated records

    form = ApplicationForm()
    applications = Application.objects.all().order_by('-id')  # Show newest first
    return render(request, 'apps/parameters/application.html', {'form': form, 'applications': applications})
    
    




##################################################################################

#  API
@login_required
def api_dhmos(request, pk):
    employee_list = Employee.objects.all().filter(organization_id=pk,is_visible=True).order_by('lastname')
    employeesSerialized = serializers.serialize('json', employee_list, ensure_ascii=False)
    return JsonResponse(json.loads(employeesSerialized), safe=False)