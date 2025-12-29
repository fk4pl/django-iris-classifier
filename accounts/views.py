from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from .forms import SignUpForm, CustomSetPasswordForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/accounts/login/')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def password_reset(request):
    if request.method == 'POST':
        form = CustomSetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = CustomSetPasswordForm(request.user)
    return render(request, 'accounts/password_reset.html', {'form': form})


@login_required
def manage_roles(request):
    if not request.user.is_staff:
        return HttpResponse('Permission denied', status=403)

    writer_group, created = Group.objects.get_or_create(name='writer')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        user = User.objects.filter(id=user_id).first()
        if user:
            if action == 'add':
                user.groups.add(writer_group)
            elif action == 'remove':
                user.groups.remove(writer_group)
        return redirect('accounts:manage_roles')

    users = User.objects.all().order_by('username')
    return render(request, 'accounts/manage_roles.html', {'users': users, 'writer_group': writer_group})
