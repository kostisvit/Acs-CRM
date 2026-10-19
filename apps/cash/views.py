from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from .models import Customer


@login_required
def customer_list(request):

    search = request.GET.get("q","")
    customer_id = request.GET.get("name", "")
    is_active = request.GET.get("is_active", "")

    customers = Customer.objects.all()

    # Active Filter
    if is_active == "true":
        customers = customers.filter(is_active=True)
    elif is_active == "fasle":
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

    page_obj = paginator.get_page(request.GET.get("page", 1))

    context = {
        "customers": page_obj,
        "search": search,
        "is_active": is_active,
        "customer_id": customer_id,
        "is_htmx": request.headers.get("HX-Request")
    }

    if request.headers.get("HX-Request"):
        return render(request, "cash/customers/_cards.html", context)

    return render(request, "cash/customers/list.html", context)
