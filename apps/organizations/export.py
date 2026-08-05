from django.http import HttpResponse
import xlwt
import datetime
from .models import Task
from .filters import ErgasiaFilter


def export_ergasies(request):
    ergasies_queryset = Task.objects.all()

    # Apply filters from GET
    filter_obj = ErgasiaFilter(request.GET, queryset=ergasies_queryset).qs
    # ErgasiaFilter(request.GET, queryset=ergasies_queryset).qs

    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = "attachment; filename=ergasies_{}.xls".format(
        datetime.date.today()
    )

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Ergasies")

    title_style = xlwt.easyxf(
        "font: bold on, height 240; align: horiz center, vert center"
    )

    ws.write(0, 0, "Πελάτης", title_style)
    ws.merge(0, 0, 0, 7)

    columns = [
        "Φορέας",
        "Ημ.Καταχ.",
        "Εφαρμογή",
        "Τύπος",
        "Υπαλ.Επικοιν.",
        "Εργασία",
        "Υπάλληλος ACS",
        "Χρόνος",
    ]

    header_style = xlwt.XFStyle()
    header_style.font.bold = True

    for col, name in enumerate(columns):
        ws.write(1, col, name, header_style)

    row_style = xlwt.XFStyle()

    row_num = 1

    for task in filter_obj:
        row_num += 1

        row = [
            task.organization.org_name if task.organization else "",
            task.importdate.strftime(
                "%d/%m/%Y") if task.importdate else "",
            task.org_app.name if task.org_app else "",
            task.job_type_acs.name if task.job_type_acs else "",
            (
                task.org_employee.lastname + " " +
                task.org_employee.firstname
                if task.org_employee else ""
            ),
            task.task_info or "",
            (
                task.acs_employee.last_name + " " +
                task.acs_employee.first_name
                if task.acs_employee else ""
            ),
            task.task_time or "",
        ]

        for col, value in enumerate(row):
            ws.write(row_num, col, value, row_style)

    wb.save(response)

    return response
