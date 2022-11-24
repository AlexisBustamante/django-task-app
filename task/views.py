from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task  # para interactuar con la BD se usa models
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)  # se crea una sesion para el usuario
                return redirect('task')

            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Usuario ya existe'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'constraseñas no coiciden'
        })


def task_completed(request):
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    # para solo las Completadas
    return render(request, 'task-completed.html', {
        'tasks': tasks
    })


@login_required
def task(request):
    # tasks = Task.objects.filter(user=request.user)  # Todas las tareas
    # para solo las pendientes
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)

    return render(request, 'task.html', {
        'tasks': tasks
    })


@login_required
def task_detail(request, task_id):

    task = get_object_or_404(Task, pk=task_id, user=request.user)
    form = TaskForm(instance=task)

    if request.method == 'GET':
        return render(request, 'task-details.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            print(request.POST)
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('task')
        except ValueError:
            return render(request, 'task-details.html', {
                'task': task,
                'form': form,
                'error': 'No fue posible Actualizar registro'
            })


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('task')


@login_required
def delete_task(request, task_id):

    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('task')


@login_required
def create_task(request):

    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })

    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('task')
        except:
            return render(request, 'create_task.html', {
                'form': TaskForm.get,
                'error': 'validate data'
            })


@login_required
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
                'error': 'User or password son incorrectos'
            })
        else:
            login(request, user)
            return redirect('task')
