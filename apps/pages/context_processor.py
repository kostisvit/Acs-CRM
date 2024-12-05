def user_companies(request):
    """
    Context processor to make user companies available globally.
    """
    if request.user.is_authenticated:
        return {'user_company': request.user.company.all()}
    return {'user_company': None}