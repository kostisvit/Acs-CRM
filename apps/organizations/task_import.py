import json
import os

import pandas as pd
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

from apps.parameters.models import JobType, OtsSoftware

from .forms import CSVUploadForm
from .models import Employee, Organization, Task

User = get_user_model()

def task_excel_import(request):
    form = CSVUploadForm()

    # ============================================================
    # PREVIEW
    # ============================================================
    if request.method == "POST" and "preview" in request.POST:

        form = CSVUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            excel_file = request.FILES["csv_file"]

            try:
                filename = excel_file.name.lower()

                if filename.endswith(".xlsx"):
                    engine = "openpyxl"

                elif filename.endswith(".xls"):
                    engine = "xlrd"

                else:
                    raise ValueError(
                        "Μη υποστηριζόμενος τύπος αρχείου. "
                        "Χρησιμοποιήστε αρχείο .xls ή .xlsx."
                    )

                df = pd.read_excel(
                    excel_file,
                    engine=engine,
                    dtype=object
                )

                df = df.fillna("")

                if "importdate" in df.columns:

                    df["importdate"] = pd.to_datetime(
                        df["importdate"],
                        errors="coerce"
                    ).dt.strftime("%d/%m/%Y")

                    df["importdate"] = df["importdate"].fillna("")

                request.session["import_data"] = df.to_json(
                    orient="records",
                    date_format="iso"
                )

                return render(
                    request,
                    "data/task_import.html",
                    {
                        "form": form,
                        "preview_data": df.to_dict(
                            orient="records"
                        ),
                        "show_import_button": True,
                    },
                )

            except Exception as e:

                messages.error(
                    request,
                    f"❌ Error reading Excel: {type(e).__name__}: {e}"
                )

    # ============================================================
    # IMPORT
    # ============================================================
    elif request.method == "POST" and "import" in request.POST:

        import_data = request.session.get("import_data")

        if not import_data:

            messages.error(
                request,
                "❌ Δεν βρέθηκαν δεδομένα για εισαγωγή. "
                "Κάντε πρώτα Preview του Excel."
            )

        else:

            try:
                data = json.loads(import_data)

                skipped_rows = 0
                skipped_rows_data = []
                import_errors = []

                for row_number, row in enumerate(data, start=2):

                    try:

                        # ==================================================
                        # ORGANIZATION
                        # ==================================================
                        organization_name = str(
                            row.get("organization", "")
                        ).strip()

                        try:
                            organization_instance = (
                                Organization.objects.get(
                                    org_name=organization_name
                                )
                            )

                        except Organization.DoesNotExist:

                            skipped_rows += 1
                            skipped_rows_data.append(row)

                            import_errors.append(
                                f"Γραμμή {row_number}: "
                                f"Ο οργανισμός '{organization_name}' "
                                f"δεν βρέθηκε."
                            )

                            continue

                        # ==================================================
                        # APPLICATION
                        # ==================================================
                        app_name = str(
                            row.get("org_app", "")
                        ).strip()

                        if app_name:

                            try:
                                app_instance = (
                                    OtsSoftware.objects.get(
                                        name=app_name
                                    )
                                )

                            except OtsSoftware.DoesNotExist:

                                app_instance = None

                        else:
                            app_instance = None

                        # ==================================================
                        # JOB TYPE
                        # ==================================================
                        job_type_name = str(
                            row.get("job_type_acs", "")
                        ).strip()

                        if job_type_name:

                            try:
                                job_type_instance = (
                                    JobType.objects.get(
                                        name=job_type_name
                                    )
                                )

                            except JobType.DoesNotExist:

                                job_type_instance = None

                        else:
                            job_type_instance = None

                        # ==================================================
                        # ACS EMPLOYEE
                        # ==================================================
                        employee_email = str(
                            row.get("employee", "")
                        ).strip().lower()

                        if not employee_email:

                            skipped_rows += 1
                            skipped_rows_data.append(row)

                            import_errors.append(
                                f"❌ Γραμμή {row_number}: "
                                f"Το πεδίο employee είναι κενό."
                            )

                            continue

                        try:

                            acs_employee_instance = User.objects.get(
                                email__iexact=employee_email
                            )

                        except User.DoesNotExist:

                            skipped_rows += 1
                            skipped_rows_data.append(row)

                            import_errors.append(
                                f"❌ Γραμμή {row_number}: "
                                f"Δεν βρέθηκε CustomUser με email "
                                f"'{employee_email}'."
                            )

                            continue

                        except User.MultipleObjectsReturned:

                            skipped_rows += 1
                            skipped_rows_data.append(row)

                            import_errors.append(
                                f"❌ Γραμμή {row_number}: "
                                f"Υπάρχουν πολλοί χρήστες με email "
                                f"'{employee_email}'."
                            )

                            continue

                        # ==================================================
                        # ORGANIZATION EMPLOYEE
                        # ==================================================
                        org_employee_instance = None

                        org_employee_name = str(
                            row.get("org_employee", "")
                        ).strip()

                        if org_employee_name:

                            try:
                                lastname, firstname = org_employee_name.split(" ", 1)

                                org_employee_instance = Employee.objects.get(
                                    lastname=lastname.strip(),
                                    firstname=firstname.strip(),
                                )

                            except Employee.DoesNotExist:

                                org_employee_instance = None

                            except ValueError:

                                org_employee_instance = None

                        # ==================================================
                        # IMPORT DATE
                        # ==================================================
                        import_date = row.get(
                            "importdate",
                            ""
                        )

                        if import_date:

                            try:

                                import_date = pd.to_datetime(
                                    import_date,
                                    errors="coerce"
                                )

                                if pd.isna(import_date):

                                    import_date = None

                                else:

                                    import_date = (
                                        import_date.date()
                                    )

                            except (
                                ValueError,
                                TypeError
                            ):

                                import_date = None

                        else:
                            import_date = None

                        # ==================================================
                        # TASK TIME
                        # ==================================================
                        task_time_raw = row.get(
                            "time",
                            ""
                        )

                        if task_time_raw in ("", None):

                            task_time = None

                        else:

                            try:

                                task_time = float(
                                    task_time_raw
                                )

                            except (
                                ValueError,
                                TypeError
                            ):

                                task_time = None

                        # ==================================================
                        # OTHER FIELDS
                        # ==================================================
                        task_info = row.get(
                            "info",
                            ""
                        )

                        task_note = row.get(
                            "text",
                            ""
                        )

                        ticketid = row.get(
                            "ticketid",
                            ""
                        )

                        # ==================================================
                        # CREATE TASK
                        # ==================================================
                        Task.objects.create(
                            organization=organization_instance,
                            importdate=import_date,
                            org_app=app_instance,
                            job_type_acs=job_type_instance,
                            task_info=task_info,
                            task_note=task_note,
                            acs_employee=acs_employee_instance,
                            task_time=task_time,
                            org_employee=org_employee_instance,
                            ticketid=ticketid,
                        )

                    # ======================================================
                    # ERROR IN SPECIFIC ROW
                    # ======================================================
                    except Exception as row_error:

                        import_errors.append(
                            f"❌ Γραμμή {row_number}: "
                            f"{type(row_error).__name__}: "
                            f"{row_error}"
                        )

                        skipped_rows += 1
                        skipped_rows_data.append(row)

                        continue

                # ============================================================
                # CLEAR IMPORT DATA
                # ============================================================
                request.session.pop(
                    "import_data",
                    None
                )

                # ============================================================
                # SAVE SKIPPED ROWS
                # ============================================================
                if skipped_rows_data:

                    skipped_df = pd.DataFrame(
                        skipped_rows_data
                    )

                    os.makedirs(
                        settings.MEDIA_ROOT,
                        exist_ok=True
                    )

                    file_path = os.path.join(
                        settings.MEDIA_ROOT,
                        "skipped_rows.xlsx"
                    )

                    skipped_df.to_excel(
                        file_path,
                        index=False
                    )

                    request.session[
                        "skipped_file_path"
                    ] = file_path

                else:

                    request.session.pop(
                        "skipped_file_path",
                        None
                    )

                # ============================================================
                # DISPLAY RESULT
                # ============================================================
                if import_errors:

                    for error in import_errors:

                        messages.error(
                            request,
                            error
                        )

                    messages.warning(
                        request,
                        (
                            f"Η εισαγωγή ολοκληρώθηκε με "
                            f"{skipped_rows} προβληματικές γραμμές. "
                            f"Οι προβληματικές γραμμές μπορούν "
                            f"να κατέβουν από το αρχείο skipped_rows.xlsx."
                        )
                    )

                else:

                    messages.success(
                        request,
                        "Η εισαγωγή ολοκληρώθηκε με επιτυχία."
                    )

                return redirect(
                    "organizations:task_excel_import"
                )

            except Exception as e:

                messages.error(
                    request,
                    (
                        f"❌ Import error: "
                        f"{type(e).__name__}: {e}"
                    )
                )

    # ============================================================
    # DEFAULT
    # ============================================================
    return render(
        request,
        "data/task_import.html",
        {
            "form": form,
            "show_download_skipped": (
                "skipped_file_path" in request.session
            ),
        },
    )
