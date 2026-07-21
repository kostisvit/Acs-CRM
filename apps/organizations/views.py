
import csv
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from openpyxl import Workbook
from apps.organizations.models import Organization
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import CSVUploadForm, OrganizationForm
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView

@login_required
def organization_list(request):

    search = request.GET.get("q", "")
    is_visible = request.GET.get("is_visible", "")

    organizations = Organization.objects.all().order_by("org_name")


    # Search filter
    if search:
        organizations = organizations.filter(
            Q(org_name__icontains=search) |
            Q(org_city__icontains=search) |
            Q(org_phone__icontains=search)
        )


    # Visibility filter
    if is_visible == "true":
        organizations = organizations.filter(
            is_visible=True
        )

    elif is_visible == "false":
        organizations = organizations.filter(
            is_visible=False
        )


    paginator = Paginator(organizations, 12)

    page_obj = paginator.get_page(
        request.GET.get("page", 1)
    )


    context = {
        "organizations": page_obj,
        "search": search,
        "is_visible": is_visible,
        "is_htmx": request.headers.get("HX-Request"),
    }
    if request.headers.get("HX-Request"):
        return render(
            request,
            "organizations/_cards.html",
            context
        )
    return render(
        request,
        "organizations/list.html",
        context
    )




class OrganizationUpdateView(SuccessMessageMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "organizations/detail.html"
    success_url = reverse_lazy("organizations:organization_list")
    success_message = "Ο πελάτης ενημερώθηκε επιτυχώς."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Επεξεργασία Πελάτη"
        return context


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
def import_customers(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)

        if form.is_valid():
            csv_file = request.FILES["csv_file"]

            if not csv_file.name.endswith(".csv"):
                messages.error(request, "Please upload a CSV file.")
                return redirect("import_customers")

            decoded = csv_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded)

            imported = 0
            errors = []

            def str_to_bool(value):
                return str(value).strip().lower() in ("true", "1", "yes", "y")

            for line, row in enumerate(reader, start=2):
                try:
                    Organization.objects.update_or_create(
                        org_name=row["name"],
                        defaults={
                            "org_address": row["address"],
                            "org_city": row["city"],
                            "org_phone": row["phone"],
                            "org_remote": row["teamviewer"],
                            "org_email": row["email"],
                            "org_site": row["website"],
                            "org_info": row["info"],
                            "is_visible": str_to_bool(row["is_visible"]),
                        },
                    )

                    imported += 1

                except Exception as e:
                    errors.append(f"Line {line}: {e}")

            # Export errors to Excel
            if errors:
                messages.warning(
                    request,
                    f"{imported} rows imported. Some rows failed. Downloading error report."
                )
                return export_errors_excel(errors)

            messages.success(
                request,
                f"{imported} customers imported successfully."
            )

            return redirect("organizations:organization_list")

    else:
        form = CSVUploadForm()

    return render(request, "data/import.html", {"form": form})