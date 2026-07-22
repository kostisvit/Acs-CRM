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
def import_csv(request, import_type):
    importer_class = IMPORTERS.get(import_type)

    if importer_class is None:
        raise Http404("Unknown import type")

    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)

        if form.is_valid():
            csv_file = request.FILES["csv_file"]

            if not csv_file.name.endswith(".csv"):
                messages.error(request, "Please upload a CSV file.")
                return redirect(request.path)

            importer = importer_class()

            imported, errors = importer.import_file(csv_file)

            if errors:
                messages.warning(
                    request,
                    f"{imported} rows imported. Some rows failed."
                )
                return export_errors_excel(errors)

            messages.success(
                request,
                f"{imported} rows imported successfully."
            )

            return redirect("organizations:organization_list")

    else:
        form = CSVUploadForm()

    return render(
        request,
        "data/import.html",
        {
            "form": form,
            "import_type": import_type,
        },
    )