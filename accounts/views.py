from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'CLIENT'
            user.save()
            login(request, user)
            return redirect('dashboard') # Redirect to dashboard after signup
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register_v3.html', {'form': form})
