from django.http import HttpResponse
from .resources import OrganizationResource
from django.shortcuts import render

def export_organization_data(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        comment_resource = OrganizationResource()
        dataset = comment_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response        
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
            return response   
    return render(request, 'app/organization/export_organization_data.html') 