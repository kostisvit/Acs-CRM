from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django_filters.views import FilterView
from .models import Organization, Employee, Ergasies, Application
from .filters import PelatisFilter, EpafiFilter, TaskFilter
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
import json
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import OrganizationModelForm,ApplicationForm
from .export import export_organization_data
from django.shortcuts import render
from django.http import HttpResponse



##################################################################################

#Λίστα πελατών
class OrganizationListView(LoginRequiredMixin,FilterView):
    model = Organization
    context_object_name = 'foreas_list'
    template_name = 'apps/organization/organization_list.html'
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
    template_name = 'apps/organization/organization_inactive.html'
    filterset_class = PelatisFilter
    ordering = ['name']
    paginate_by = 10  

    def get_queryset(self):
        """
        Use the custom manager to filter inactive records (is_visible=False).
        """
        return Organization.objects.invisible()

from django.contrib import messages
def create_organization(request):
    if request.method == 'POST':
        # Print the POST data to check what has been submitted
        print(request.POST)  # Debug: print all submitted data

        # Create the form with the submitted data
        form = OrganizationModelForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # Save the form if valid
            form.save()

            # Add a success message
            messages.success(request, 'Ο οργανισμός δημιουργήθηκε με επιτυχία!')

            return redirect('organization-create')  # Redirect to a success page after saving
        else:
            # If the form is not valid, print the form errors
            print(form.errors)  # Debug: print form errors

            # Optionally, print each field's specific error:
            for field, errors in form.errors.items():
                print(f"Error in {field}: {errors}")

    else:
        # If the request method is GET, just instantiate an empty form
        form = OrganizationModelForm()

    return render(request, 'apps/organization/organization_new_form.html', {'form': form}) # Adjust the URL as needed

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
    template_name = 'apps/organization/organization_contact.html'
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
    context_object_name = 'tasks_list'
    template_name = 'apps/organization/organization_tasks.html'
    filterset_class = TaskFilter
    ordering = ['importdate']
    paginate_by = 10

##################################################################################



def application_view(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('application_view')  # Reload to display updated records

    form = ApplicationForm()
    applications = Application.objects.all().order_by('-id')  # Show newest first
    return render(request, 'apps/parameters/application.html', {'form': form, 'applications': applications})