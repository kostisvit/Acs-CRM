from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import EmailLoginForm,CustomPasswordChangeForm
from django.contrib.auth import get_user_model

from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

User = get_user_model()


def login_view(request):
    if request.method == "POST":
        form = EmailLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)

                if user.must_change_password:
                    return redirect("accounts:change_password")

                return redirect("home")

            form.add_error(None, "Invalid email or password")

    else:
        form = EmailLoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):

    logout(request)
    return redirect("accounts:login")


def users_view(request):
    users = User.objects.all()
    return render(request, "accounts/users.html", {"users": users})



class FirstPasswordChangeView(PasswordChangeView):
    template_name = "registration/change_password.html"
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)

        self.request.user.must_change_password = False
        self.request.user.save(update_fields=["must_change_password"])

        return response