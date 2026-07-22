from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from openpyxl import Workbook
from apps.organizations.forms import CSVUploadForm
from .importers import IMPORTERS
from django.http import Http404





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