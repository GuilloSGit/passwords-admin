from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import CreatePasswordForm
from .models import Password
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def home(request):
    userName = request.user.username
    return render(request, 'home.html', {
        'userName': userName
    })


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('passwords')

            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Passwords do not match each other'
        })


@login_required
def passwords(request):
    owned_list = Password.objects.filter(user=request.user, active=True)
    received_list = Password.objects.filter(
        shared=True, sharedWith=request.user, active=True)
    return render(request, 'passwords.html', {
        'on_passwords_page': True,
        'owned_list': owned_list,
        'received_list': received_list
    })


@login_required
def create_password(request):
    if request.method == 'GET':
        form = CreatePasswordForm(user=request.user)
        return render(request, 'create_password.html', {
            'form': form,
        })
    else:
        try:
            form = CreatePasswordForm(request.POST, user=request.user)
            if form.is_valid():
                new_password = form.save(commit=False)
                new_password.user = request.user
                new_password.save()

                if new_password.shared:
                    new_password.sharedWith.set(
                        form.cleaned_data['sharedWith'])
                else:
                    # Limpiar si no es compartido.
                    new_password.sharedWith.clear()

                return redirect('passwords')
            else:
                return render(request, 'create_password.html', {
                    'form': form,
                    'error': 'Invalid data'
                })
        except ValueError:
            return render(request, 'create_password.html', {
                'form': CreatePasswordForm(user=request.user),
                'error': 'Invalid data'
            })


@login_required
def password_edit(request, password_id):
    password = get_object_or_404(Password, pk=password_id, user=request.user)

    if request.method == 'GET':
        form = CreatePasswordForm(instance=password, user=request.user)
        return render(request, 'password_edit.html', {
            'password': password,
            'form': form
        })
    else:
        form = CreatePasswordForm(
            request.POST, instance=password, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('passwords')
        else:
            return render(request, 'password_edit.html', {
                'password': password,
                'form': form
            })


@login_required
def password_detail(request, password_id):
    try:
        password = Password.objects.get(pk=password_id)
        if password.user != request.user and request.user not in password.sharedWith.all():
            return redirect('access_denied')
        return render(request, 'password_detail.html', {'password': password})
    except Password.DoesNotExist:
        return redirect('access_denied')


@login_required
def password_delete(request, password_id):
    password = get_object_or_404(Password, pk=password_id, user=request.user)

    if request.method == 'POST':
        password.active = False
        password.save()
        return redirect('passwords')

    return render(request, 'password_confirm_delete.html', {
        'password': password
    })


@login_required
def access_denied(request):
    return render(request, 'access_denied.html')


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username and/or password incorrect'
            })

        else:
            login(request, user)
            return redirect('passwords')
