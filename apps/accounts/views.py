from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import EmailAuthenticationForm, UserUpdateForm
from .password_change import password_change
from django_filters.views import FilterView
from django.views.generic import TemplateView
from .models import Adeia
from .filters import AdeiaFilter

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
                return redirect('home')  # Redirect to home page after successful login
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
class AdeiaListView(LoginRequiredMixin,FilterView):
    model = Adeia
    template_name = "apps/accounts/adeia.html"
    context_object_name = "adeia_list"
    filterset_class = AdeiaFilter
    ordering = ['created']
    pagination = 10



class AcsProfile(LoginRequiredMixin,TemplateView):
    template_name = "apps/accounts/profile.html"




from django.contrib import messages

def update_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your phone number has been updated.')
            return redirect('profile')  # Change 'profile' to your desired redirect URL
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'apps/accounts/profile.html', {'form': form})



