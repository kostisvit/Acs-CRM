from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import EmailLoginForm,CustomPasswordChangeForm
from django.contrib.auth import get_user_model
from .models import Adeia
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from datetime import date
import datetime

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


from django.db.models import F, ExpressionWrapper, DurationField

class MyLeaveListView(LoginRequiredMixin, ListView):

    model = Adeia
    template_name = "accounts/adeia_dashboard.html"
    context_object_name = "adeia_list"
    paginate_by = 10


    def get_queryset(self):
        today = datetime.date.today()
        return (
            Adeia.objects
            
            .filter(
                acs_employee=self.request.user,startdate__year=today.year
            )
            .select_related(
                "acs_adeiatype"
            )
            .order_by("-startdate")
        )


    def get_year_leave_total(self, employee, year=None):

        if year is None:
            year = date.today().year


        leaves = (
            Adeia.objects
            .filter(
                acs_employee=employee,
                startdate__year=year
            )
            .select_related(
                "acs_adeiatype"
            )
        )


        return sum(
            leave.working_days()
            for leave in leaves
        )


    def get_leave_total(self, employee, leave_type, year=None):

        if year is None:
            year = date.today().year


        leaves = (
            Adeia.objects
            .filter(
                acs_employee=employee,
                startdate__year=year,
                acs_adeiatype__name=leave_type
            )
        )


        return sum(
            leave.working_days()
            for leave in leaves
        )



    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)


        employee = self.request.user


        # Leave types summary

        context["adeia_total"] = self.get_leave_total(
            employee,
            "Κανονική"
        )


        context["adeia_anarotiki_total"] = self.get_leave_total(
            employee,
            "Αναρρωτική"
        )


        context["adeia_eortastiki_total"] = self.get_leave_total(
            employee,
            "Εορταστική"
        )


        context["adeia_kioforias_total"] = self.get_leave_total(
            employee,
            "Κυοφορίας"
        )


        context["adeia_mitrothtas_total"] = self.get_leave_total(
            employee,
            "Μητρότητας"
        )


        context["adeia_patrothtas_total"] = self.get_leave_total(
            employee,
            "Πατρότητας"
        )


        context["adeia_gamou_total"] = self.get_leave_total(
            employee,
            "Γάμου"
        )


        context["adeia_goniki_total"] = self.get_leave_total(
            employee,
            "Γονική"
        )


        context["adeia_anef_apodoxon_total"] = self.get_leave_total(
            employee,
            "Άνευ Αποδοχών"
        )



        # Annual leave balance

        allowed_days = employee.allowed_leave_days


        used_days = self.get_leave_total(
            employee,
            "Κανονική"
        )


        context["days_sum"] = allowed_days

        context["days_used"] = used_days

        context["days_left"] = max(
            allowed_days - used_days,
            0
        )


        # percentage for progress bar

        context["leave_percentage"] = (
            round(
                (used_days / allowed_days) * 100,
                2
            )
            if allowed_days
            else 0
        )


        return context