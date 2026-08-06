import datetime
from django.http import HttpResponse
import xlwt
from .filters import DayOffFilter
from .models import Adeia

# export άδειες χρήστη


def export_adeia(request):
    today = datetime.date.today()
    adeia_queryset = Adeia.objects.filter(
        created__year=today.year, acs_employee=request.user).select_related("acs_employee", "acs_adeiatype")
    filter_adeies = DayOffFilter(request.GET, queryset=adeia_queryset).qs
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = (
        f"attachment; filename=adeies_{today}.xls"
    )
    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Adeia")
    columns = [
        "ACS",
        "Τύπος άδειας",
        "Αρχή",
        "Τέλος",
        "Ημέρες",
        "Καταγραφή",
    ]
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    for adeia in filter_adeies:
        row_num += 1
        row = [
            f"{adeia.acs_employee.last_name} {adeia.acs_employee.first_name}",
            adeia.acs_adeiatype.name,
            adeia.startdate.strftime("%d/%m/%Y") if adeia.startdate else "",
            adeia.enddate.strftime("%d/%m/%Y") if adeia.enddate else "",
            adeia.working_days(),
            adeia.created.strftime("%d/%m/%Y"),
        ]
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)

    return response
