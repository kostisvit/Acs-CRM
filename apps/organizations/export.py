import datetime

import xlwt
from django.http import HttpResponse

from .filters import ErgasiaFilter
from .models import Task


def export_ergasies(request):
    queryset = (
        Task.objects
        .select_related(
            "organization",
            "org_app",
            "job_type_acs",
            "acs_employee",
            "org_employee",
        )
        .order_by("-importdate", "-pk")
    )

    task_filter = ErgasiaFilter(
        request.GET,
        queryset=queryset,
    )

    tasks = task_filter.qs

    response = HttpResponse(
        content_type="application/vnd.ms-excel"
    )

    filename = (
        f"ergasies_organismou_{datetime.date.today()}.xls"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{filename}"'
    )

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Ergasies")

    # -----------------------------
    # Styles
    # -----------------------------

    # Title
    title_style = xlwt.easyxf(
        "font: bold on, color white, height 240; "
        "pattern: pattern solid, fore_colour dark_blue; "
        "align: horiz center, vert center"
    )

    # Header
    header_style = xlwt.easyxf(
        "font: bold on, color white; "
        "pattern: pattern solid, fore_colour blue; "
        "align: horiz center, vert center; "
        "borders: "
        "left thin, right thin, top thin, bottom thin"
    )

    # Normal cells
    cell_style = xlwt.easyxf(
        "align: vert center; "
        "borders: "
        "left thin, right thin, top thin, bottom thin"
    )

    # Alternate row
    alternate_style = xlwt.easyxf(
        "pattern: pattern solid, fore_colour ice_blue; "
        "align: vert center; "
        "borders: "
        "left thin, right thin, top thin, bottom thin"
    )

    organization_name = ""

    first_task = tasks.first()
    if first_task and first_task.organization:
        organization_name = first_task.organization.org_name

    ws.write(
        0,
        0,
        f"Οργανισμός: {organization_name}",
        title_style
    )
    ws.merge(0, 0, 0, 8)

    columns = [
        "Οργανισμός",
        "Καταχώρηση",
        "Εφαρμογή",
        "Τύπος Εργασίας",
        "Υπαλ.Οργανισμού",
        "Εργασία",
        "ACS",
        "Διάρκεια",
        "Ημ.Δημιουργίας",
    ]

    header_style = xlwt.XFStyle()
    header_style.font.bold = True

    for col, name in enumerate(columns):
        ws.write(1, col, name, header_style)

    row_num = 1

    for task in tasks:
        row_num += 1

        row = [
            (
                task.organization.org_name
                if task.organization
                else ""
            ),
            (
                task.importdate.strftime("%d/%m/%Y")
                if task.importdate
                else ""
            ),
            (
                task.org_app.name
                if task.org_app
                else ""
            ),
            (
                task.job_type_acs.name
                if task.job_type_acs
                else ""
            ),
            (
                f"{task.org_employee.lastname} "
                f"{task.org_employee.firstname}"
                if task.org_employee
                else ""
            ),
            task.task_info or "",
            (
                f"{task.acs_employee.last_name} "
                f"{task.acs_employee.first_name}"
                if task.acs_employee
                else ""
            ),
            task.task_time or "",
            (
                task.created.strftime("%d/%m/%Y %H:%M:%S")
                if task.created
                else ""
            ),
        ]
    # Alternate row colors
        current_style = (
            alternate_style
            if row_num % 2 == 0
            else cell_style
        )
        for col, value in enumerate(row):
            ws.write(row_num, col, value, current_style)

    wb.save(response)

    return response

