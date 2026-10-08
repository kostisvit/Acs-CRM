from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from .filters import CustomerFilter
from .models import Customer


@login_required
def customer_list(request):
    if request.method == "POST":
        mode = request.POST.get("view_mode")

        if mode in ["cards", "table"]:
            request.session["customer_view"] = mode

    queryset = (
        Customer.objects
        .select_related(
            "organization",
            "org_app",
            "job_type_acs",
            "acs_employee",
            "org_employee",
        )
        .order_by("-importdate", "-pk")
    )

    customer_filter = CustomerFilter(
        request.GET,
        queryset=queryset,
    )

    # All records / filtered records
    customers = customer_filter.qs

    # Check whether at least one actual filter was selected
    # has_filters = any(
    #     value.strip()
    #     for key, value in request.GET.items()
    #     if key != "page" and value.strip()
    # )

    # if has_filters:
    #     task_count_by_organization = tasks.count()

    #     task_time_by_organization = (
    #         tasks.aggregate(
    #             total=Sum("task_time")
    #         )["total"] or Decimal("0")
    #     )
    # else:
    #     task_count_by_organization = 0
    #     task_time_by_organization = Decimal("0")

    paginator = Paginator(customers, 12)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop("page", None)

    query_string = query_params.urlencode()
    context = {
        "filter": customer_filter,
        "customers": page_obj,
        "page_obj": page_obj,
        "query_string": query_string,
        "is_htmx": request.headers.get("HX-Request"),
    }

    if request.headers.get("HX-Request"):

        # "Περισσότερα"
        if request.GET.get("page"):
            return render(
                request,
                "tameiakes/_customer_load_more_response.html",
                context,
            )

        # Filter / search
        return render(
            request,
            "tameiakes/_customer_results.html",
            context,
        )

    return render(
        request,
        "tameiakes/list.html",
        context,
    )
