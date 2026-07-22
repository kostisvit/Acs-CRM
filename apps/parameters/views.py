from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from openpyxl import Workbook
from .importers import IMPORTERS
from .models import JobType, OtsSoftware
import json
from django.http import JsonResponse


@login_required
def parameters_view(request):
    return render(
        request,
        "parameters/parameters.html",

    )

@login_required
def jobtype_view(request):
    job_types =  JobType.objects.all()
    return render(
        request,
        "parameters/_job_type.html",
        {
            "job_types": job_types
        }

    )

def add_job_type(request):

    data = json.loads(request.body)


    job_type = JobType.objects.create(
        name=data["name"],
        is_active=data.get("is_active", True)
    )


    return JsonResponse({
        "id": job_type.id,
        "name": job_type.name,
        "is_active": job_type.is_active
    })




@login_required
def ots_software_view(request):
    ots_software = OtsSoftware.objects.all()
    return render(
        request,
        "parameters/_ots_software.html",
        {
            "ots_software": ots_software
        }

    )


@login_required
def export_errors_excel(errors):
    wb = Workbook()
    ws = wb.active
    ws.title = "Import Errors"

    # Header
    ws.append(["Line", "Error"])

    # Data
    for error in errors:
        line, message = error.split(": ", 1)
        ws.append([line.replace("Line ", ""), message])

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    response["Content-Disposition"] = 'attachment; filename="import_errors.xlsx"'

    return response


@login_required
def import_csv(request):
    if request.method == "POST":
        importer_name = request.POST.get("importer")

        importer_data = IMPORTERS.get(importer_name)

        if not importer_data:
            messages.error(request, "Invalid importer")
            return redirect("parameters:import")

        csv_file = request.FILES.get("file")

        if not csv_file:
            messages.error(request, "No CSV file selected")
            return redirect("parameters:import")

        importer_class = importer_data["class"]

        importer = importer_class()
        imported, errors = importer.import_file(csv_file)

        messages.success(
            request,
            f"Imported {imported} records"
        )

        if errors:
            messages.warning(
                request,
                "\n".join(errors)
            )

        return redirect("parameters:import")

    return render(
        request,
        "data/import.html",
        {
            "importers": IMPORTERS
        }
    )