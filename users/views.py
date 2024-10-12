from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Profile, Enrollment
from main.models import Course

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт был создан! Войти сейчас!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {
        'form': form
        }
    return render(request, 'users/register.html', context=context)


def logout_view(request):
    logout(request)
    return render(request, 'users/logout.html')


@login_required
def profile(request):

    enrollments = Enrollment.objects.filter(user=request.user)
    courses = [enrollment.course for enrollment in enrollments]

    context = {
        'u_form': ProfileUpdateForm(instance=request.user),
        'courses': courses,
    }
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = ProfileUpdateForm(request.POST, instance=request.user)

        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Account has been updated!')
            return redirect('profile')
    else:
        u_form = ProfileUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
    }

    return render(request, 'users/edit_profile.html', context)
