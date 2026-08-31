import json
from io import BytesIO
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from openpyxl import Workbook
from .importers import IMPORTERS
from .models import JobType, OtsSoftware, OrgDepartment, AcsAdeia, TrainingType



@login_required
def parameters_view(request):
    return render(
        request,
        "parameters/parameters.html",
    )


# Job type view and create job type view


@login_required
def jobtype_view(request):
    job_types = JobType.objects.all()
    return render(request, "parameters/_job_type.html", {"job_types": job_types})


def add_job_type(request):
    data = json.loads(request.body)
    job_type = JobType.objects.create(name=data["name"], is_active=data.get("is_active", True))
    return JsonResponse({"name": job_type.name, "is_active": job_type.is_active})


# Ots software view


@login_required
def ots_software_view(request):
    ots_software = OtsSoftware.objects.all()
    return render(request, "parameters/_ots_software.html", {"ots_software": ots_software})


# Organization department view


@login_required
def org_department_view(request):
    org_department = OrgDepartment.objects.all()
    return render(request, "parameters/_org_department.html", {"org_department": org_department})


# Acs adeia type
@login_required
def acs_adeia_type_view(request):
    acs_adeia_type = AcsAdeia.objects.all()
    return render(request, "parameters/_acs_adeia_type.html", {"acs_adeia_type": acs_adeia_type})


# Training type view
@login_required
def training_type_view(request):
    training_types = TrainingType.objects.all()
    return render(request, "parameters/_training_type.html", {"training_types": training_types})


# Import csv view


def export_errors_excel(errors):
    wb = Workbook()
    ws = wb.active
    ws.title = "Import Errors"

    ws.append(["Line", "Error"])

    for error in errors:
        line = error.get("line", "")
        message = error.get("error", "")

        ws.append([line, message])

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
        result = importer.import_file(csv_file)

        imported = result["imported"]
        csv_records = result["csv_records"]
        errors = result["errors"]

        if imported < csv_records:
            messages.warning(
                request,
                f"Imported {imported}/{csv_records} records. "
                f"{csv_records - imported} records failed.",
            )

            # Export failed rows
            return export_errors_excel(errors)

        messages.success(request, f"Successfully imported all {imported} records")

        return redirect("parameters:import")

    return render(
        request,
        "data/import.html",
        {
            "importers": dict(
                sorted(
                    IMPORTERS.items(),
                    key=lambda item: item[1]["label"] if "label" in item[1] else item[0],
                )
            )
        },
    )
