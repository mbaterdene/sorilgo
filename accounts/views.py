from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib import messages
from .forms import SignUpForm
from .tokens import account_activation_token




def signup_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.username = form.cleaned_data.get('username')
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.user_info.phone = form.cleaned_data.get('phone_number')
            user.user_info.gender = form.cleaned_data.get('gender')
            user.whatsgrade.is_grade = form.cleaned_data.get('grade')
            user.user_info.add_info = form.cleaned_data.get('add_info')
            user.is_active = True
            user.is_staff = False
            user.is_superuser = False
            user.save()
            return redirect('login_ok')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
