from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    first_name = request.user.first_name if request.user.is_authenticated else "Guest"
    return render(request, "home.html", {"first_name": first_name})
