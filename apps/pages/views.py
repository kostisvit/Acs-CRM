from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def homePageView(request):
    user = request.user  # get the logged-in user
    return render(request, 'home.html', {'user': user})
