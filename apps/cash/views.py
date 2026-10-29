from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from .models import CashRegister, Customer


@login_required
def customer_list(request):
    if request.method == "POST":
        mode = request.POST.get("view_mode")

        if mode in ["cards", "table"]:
            request.session["customer_view"] = mode

    search = request.GET.get("q","")
    customer_id = request.GET.get("name", "")
    is_active = request.GET.get("is_active", "")

    customers = Customer.objects.all()

    # Active Filter
    if is_active == "true":
        customers = customers.filter(is_active=True)
    elif is_active == "false":
        customers = customers.filter(is_active=False)
    else:
        customers = customers.filter(is_active=True)

    if search:
        customers = customers.filter(
            Q(name__icontains=search)
            | Q(vat_number__icontains=search)
        )

    if customer_id:
        customers = customers.filter(id=customer_id)

    customers = customers.order_by("name")

    paginator = Paginator(customers, 12)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop("page", None)

    query_string = query_params.urlencode()

    context = {
        "customers": page_obj,
        "page_obj": page_obj,
        "search": search,
        "is_active": is_active,
        "query_string": query_string,
        "customer_id": customer_id,
        "is_htmx": request.headers.get("HX-Request")
    }

    if request.headers.get("HX-Request"):

            # "Περισσότερα"
            if request.GET.get("page"):
                return render(
                    request,
                    "cash/customers/_customer_load_more_response.html",
                    context,
                )

            # Filter / search
            return render(
                request,
                "cash/customers/_customer_results.html",
                context,
            )

    return render(
            request,
            "cash/customers/list.html",
            context,
        )


@login_required
def cash_list(request):
    if request.method == "POST":
        mode = request.POST.get("view_mode")

        if mode in ["cards", "table"]:
            request.session["customer_view"] = mode

    search = request.GET.get("q","")
    cash_id = request.GET.get("serial_number", "")

    cash_list = CashRegister.objects.all()

    # Active Filter
    # if is_active == "true":
    #     customers = customers.filter(is_active=True)
    # elif is_active == "false":
    #     customers = customers.filter(is_active=False)
    # else:
    #     customers = customers.filter(is_active=True)

    if search:
        cash_list = cash_list.filter(
            Q(serial_number__icontains=search)
        )

    if cash_id:
        cash_list = cash_list.filter(id=cash_id)

    cash_list = cash_list.order_by("-created")

    paginator = Paginator(cash_list, 12)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop("page", None)

    query_string = query_params.urlencode()

    context = {
        "cash_list": page_obj,
        "page_obj": page_obj,
        "search": search,
        "query_string": query_string,
        "cash_id": cash_id,
        "is_htmx": request.headers.get("HX-Request")
    }

    # if request.headers.get("HX-Request"):

    #         # "Περισσότερα"
    #         if request.GET.get("page"):
    #             return render(
    #                 request,
    #                 "cash/customers/_customer_load_more_response.html",
    #                 context,
    #             )

    #         # Filter / search
    #         return render(
    #             request,
    #             "cash/customers/_customer_results.html",
    #             context,
    #         )

    return render(
            request,
            "cash/customers/_cash_list.html",
            context,
        )
