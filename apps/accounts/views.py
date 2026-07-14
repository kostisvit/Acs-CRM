from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .forms import EmailLoginForm


def login_view(request):
    if request.method == "POST":
        form = EmailLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                return redirect("home")

            form.add_error(None, "Invalid email or password")

    else:
        form = EmailLoginForm()

    return render(request, "accounts/login.html", {"form": form})
