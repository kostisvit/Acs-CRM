from apps.cash.models import CashRegister, Customer


# Count online Customers
def customers_online_count(request):
    if request.user.is_authenticated:
        return {"total_online_customers": Customer.objects.filter(is_active=True).count()}
    total_online_customers = 0
    return {'total_online_customers': total_online_customers}


# Count online Cash
def cash_register_online_count(request):
    if request.user.is_authenticated:
        return {"total_online_cash_register": CashRegister.objects.filter(status=CashRegister.Status.ACTIVE).count()}
    total_online_cash_register = 0
    return {'total_online_cash_register': total_online_cash_register}
