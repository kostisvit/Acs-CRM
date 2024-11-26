from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from .models import Dhmos
from .filters import PelatisFilter

class ForeasListView(LoginRequiredMixin,FilterView):
    model = Dhmos
    context_object_name = 'foreas_list'
    template_name = 'apps/foreas/foreas.html'
    filterset_class = PelatisFilter
    ordering = ['name']
    paginate_by = 10
