from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django_filters.views import FilterView
from .models import Dhmos, Employee
from .filters import PelatisFilter, EpafiFilter
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
import json


#Λίστα πελατών
class ForeasListView(LoginRequiredMixin,FilterView):
    model = Dhmos
    context_object_name = 'foreas_list'
    template_name = 'apps/foreas/foreas.html'
    filterset_class = PelatisFilter
    ordering = ['name']
    paginate_by = 10

    def get_queryset(self):
        """
        Use the custom manager to filter inactive records (is_visible=False).
        """
        return Dhmos.objects.visible()


class ForeasListViewVisibleFalse(LoginRequiredMixin,FilterView):
    model = Dhmos
    context_object_name = 'foreas_list'
    template_name = 'apps/foreas/foreas_in_active.html'
    filterset_class = PelatisFilter
    ordering = ['name']
    paginate_by = 10  

    def get_queryset(self):
        """
        Use the custom manager to filter inactive records (is_visible=False).
        """
        return Dhmos.objects.invisible()

#Διόρθωση εγγραφών πελατών
@login_required
def edit_forea(request, dhmos_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        dhmos = get_object_or_404(Dhmos, id=dhmos_id)
        dhmos.name = data.get('name')
        dhmos.address = data.get('address')
        dhmos.city = data.get('city')
        dhmos.phone = data.get('phone')
        dhmos.email = data.get('email')
        dhmos.website = data.get('website')
        dhmos.is_visible = data.get('is_visible')
        dhmos.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed'}, status=400)


def soft_delete_dhmos(request, pk):
    """Soft delete"""
    dhmos = get_object_or_404(Dhmos, pk=pk)
    dhmos.delete()
    return redirect('pelatis')

def restore_dhmos(request, pk):
    """Restore a soft-deleted product."""
    dhmos = get_object_or_404(Dhmos, pk=pk)
    dhmos.restore()
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