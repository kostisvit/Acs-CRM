from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django_filters.views import FilterView
from .models import Organization, Employee, Ergasies
from .filters import PelatisFilter, EpafiFilter, TaskFilter
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
import json

##################################################################################

#Λίστα πελατών
class OrganizationListView(LoginRequiredMixin,FilterView):
    model = Organization
    context_object_name = 'foreas_list'
    template_name = 'apps/foreas/foreas.html'
    filterset_class = PelatisFilter
    ordering = ['name']
    paginate_by = 10

    def get_queryset(self):
        """
        Use the custom manager to filter inactive records (is_visible=False).
        """
        return Organization.objects.visible()


class OrganizationListViewVisibleFalse(LoginRequiredMixin,FilterView):
    model = Organization
    context_object_name = 'foreas_list'
    template_name = 'apps/foreas/foreas_in_active.html'
    filterset_class = PelatisFilter
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
        organization.is_visible = data.get('is_visible')
        organization.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed'}, status=400)


def soft_delete_organization(request, pk):
    """Soft delete"""
    organization = get_object_or_404(Organization, pk=pk)
    organization.delete()
    return redirect('pelatis')

def restore_organization(request, pk):
    """Restore a soft-deleted product."""
    organization = get_object_or_404(Organization, pk=pk)
    organization.restore()
    return redirect('pelatis')

##################################################################################

# Λίστα επαφών
class EpafiListView(LoginRequiredMixin, FilterView):
    model = Employee
    context_object_name = 'epafi_list'
    template_name = 'apps/foreas/contact.html'
    filterset_class = EpafiFilter
    ordering = ['lastname']
    paginate_by = 9

    def get_queryset(self):
        """
        Use the custom manager to filter inactive records (is_visible=False).
        """
        return Employee.objects.visible()


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
    return redirect('contact')

def restore_contact(request, pk):
    """Restore a soft-deleted product."""
    employee = get_object_or_404(Employee, pk=pk)
    employee.restore()
    return redirect('contact')

##################################################################################

# Λίστα Εργασιών Οργανισμού

class OrganizationTasks(LoginRequiredMixin, FilterView):
    model = Ergasies
    #context_object_name = 'tasks_list'
    template_name = 'apps/foreas/tasks.html'
    filterset_class = TaskFilter
    ordering = ['importdate']


from django.shortcuts import render
from django.http import HttpResponse
from .forms import ApplicationForm
from .models import Application

def application_view(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('application_view')  # Reload to display updated records

    form = ApplicationForm()
    applications = Application.objects.all().order_by('-id')  # Show newest first
    return render(request, 'apps/parameters/application.html', {'form': form, 'applications': applications})