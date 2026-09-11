import json
import os
from datetime import datetime

import pandas as pd
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from apps.parameters.models import JobType, OtsSoftware

from .forms import CSVUploadForm
from .models import Employee, Organization, Task


def task_excel_import(request):
    form = CSVUploadForm()  # Always initialize the form
    if request.method == "POST" and "preview" in request.POST:
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES["file"]
            try:
                df = pd.read_excel(excel_file)
                df.fillna("", inplace=True)  # Replace NaNs with empty strings

                # Save raw data to session for confirmation step
                request.session["import_data"] = df.to_json(orient="records", date_format="iso")
                return render(
                    request,
                    "data/task_import.html",
                    {
                        "form": form,
                        "preview_data": df.to_dict(orient="records"),
                        "show_import_button": True,
                    },
                )
            except Exception as e:
                messages.error(request, f"Error reading file: {e}")

    elif request.method == "POST" and "import" in request.POST:
        import_data = request.session.get("import_data")
        if import_data:
            try:
                data = json.loads(import_data)
                skipped_rows = 0
                skipped_rows_data = []

                for row in data:
                    try:
                        organization_instance = Organization.objects.get(name=row["organization"])
                    except Organization.DoesNotExist:
                        skipped_rows += 1
                        skipped_rows_data.append(row)
                        continue

                    # Optional foreign key lookups
                    try:
                        app_instance = OtsSoftware.objects.get(name=row["org_app"])
                    except OtsSoftware.DoesNotExist:
                        app_instance = None

                    try:
                        job_type_instance = JobType.objects.get(name=row["job_type_acs"])
                    except JobType.DoesNotExist:
                        job_type_instance = None

                    try:
                        acs_employee_instance = User.objects.get(username=row["employee"])
                    except User.DoesNotExist:
                        acs_employee_instance = None

                    try:
                        lastname, firstname = row["org_employee"].strip().split(" ", 1)
                        org_employee_instance = Employee.objects.get(lastname=lastname, firstname=firstname)
                    except (Employee.DoesNotExist, ValueError):
                        org_employee_instance = None

                    Task.objects.create(
                        dhmos=organization_instance,
                        importdate=datetime.fromisoformat(row["importdate"]).date() if row["importdate"] else None,
                        org_app=app_instance,
                        job_type_acs=job_type_instance,
                        task_info=row["info"],
                        task_note=row["text"],
                        acs_employee=acs_employee_instance,
                        task_time=row["time"],
                        org_employee=org_employee_instance,
                        ticketid=row["ticketid"],
                    )

                # Clear session data
                del request.session["import_data"]

                # Save skipped rows to file if any
                if skipped_rows_data:
                    skipped_df = pd.DataFrame(skipped_rows_data)
                    file_path = os.path.join(settings.MEDIA_ROOT, "skipped_rows.xlsx")
                    skipped_df.to_excel(file_path, index=False)
                    request.session["skipped_file_path"] = file_path
                    messages.warning(
                        request,
                        f"Η εισαγωγή ολοκληρώθηκε με παράλειψη {skipped_rows} γραμμής/ών. Μπορείτε να τις κατεβάσετε παρακάτω.",
                    )
                else:
                    request.session.pop("skipped_file_path", None)
                    messages.success(request, "Η εισαγωγή ολοκληρώθηκε με επιτυχία.")

                return redirect("import_excel")

            except Exception as e:
                messages.error(request, f"Import error: {e}")

    else:
        form = CSVUploadForm()

    return render(
        request,
        "data/task_import.html",
        {"form": form, "show_download_skipped": "skipped_file_path" in request.session},
    )
