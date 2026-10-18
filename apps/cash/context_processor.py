from apps.cash.models import Customer


def customers_count(request):
    if request.user.is_authenticated:
        return {"total_online_customers": Customer.objects.filter(is_active=True).count()}
    total_online_customers = 0
    return {'total_online_customers': total_online_customers}
