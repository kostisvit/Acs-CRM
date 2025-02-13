from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import AdeiaForm, EmailAuthenticationForm, UserUpdateForm
from .password_change import password_change
from django_filters.views import FilterView
from django.views.generic import TemplateView
from .models import Adeia
from .filters import AdeiaFilter
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
import datetime

# Login user function


def custom_login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect to home page after successful login
                return redirect('home')
        else:
            # If the form is invalid, the error message will be shown on the form
            return render(request, 'apps/accounts/login.html', {'form': form})
    else:
        form = EmailAuthenticationForm()
    return render(request, 'apps/accounts/login.html', {'form': form})


# Logout user function
def custom_logout(request):
    logout(request)
    return redirect('login')


##########################################################################

def adeia_list(request):
    today = datetime.date.today()

    adeia_list = Adeia.objects.filter(
        startdate__year=today.year, acs_employee=request.user)
    adeia_filter = AdeiaFilter(request.GET, queryset=adeia_list)

    paginator = Paginator(adeia_filter.qs, 10)  # 10 tasks per page
    # Get the page number from the request
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Copy request.GET to preserve existing filters
    filter_params = request.GET.copy()
    if filter_params.get('page'):
        filter_params.pop('page')
    form = AdeiaForm()
    show_modal = False
    if request.method == "POST":
        form = AdeiaForm(request.POST)
        if form.is_valid():
            form.author = request.user
            form.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = AdeiaForm(initial={'acs_employee': request.user})

    context = {
        'adeia_list': page_obj,
        'filter': adeia_filter,
        'filter_params': filter_params.urlencode(),
        'form': form,
        'show_modal': show_modal,
    }
    return render(request, 'apps/accounts/adeia.html', context)


class AcsProfile(LoginRequiredMixin, TemplateView):
    template_name = "apps/accounts/profile.html"


def update_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your phone number has been updated.')
            # Change 'profile' to your desired redirect URL
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'apps/accounts/profile.html', {'form': form})
