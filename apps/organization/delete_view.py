from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from .models import Ergasies

class ErgasiesDeleteView(DeleteView):
    model = Ergasies
    success_url = reverse_lazy('tasks')
    template_name = 'apps/organization/task_confirm_delete.html'
    

