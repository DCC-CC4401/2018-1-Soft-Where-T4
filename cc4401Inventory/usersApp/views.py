from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from mainApp.models import User
from django.http import HttpResponse, HttpResponseRedirect


def login_view(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'usersApp/login.html', context=context)
    if request.method == 'POST':
        pass

#se llama cuando se envia el formulario de login
def login_submit(request):

    username = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    context = {'error_message': ''}

    if user is not None:
        login(request, user)

        context = {'user':user}
        #aca hay que redirigir a la pagina de inicio del usuario
        return redirect('/articles/')

    else:
        error_message = 'La contraseña ingresada no es correcta o el usuario no existe'
        context['error_message'] = error_message
        return render(request, 'usersApp/login.html', context=context)

#se llama cuando se quiere acceder a la pagina de creacion de cuentas
def signup(request):
    if request.method == 'GET':
        return render(request, 'usersApp/create_account.html')
    if request.method == 'POST':
        pass

#se llama cuando se manda el formulario de creacion de cuentas
def signup_submit(request):

    context = {'error_message': '', }

    if(request.method == 'POST'):
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']

        if User.objects.filter(email = email).exists():
            error_message = 'Ya existe una cuenta con ese correo.'
            context['error_message'] = error_message
            return render(request, 'usersApp/create_account.html', context=context)
        else:
            user = User.objects.create_user(first_name=first_name, email=email, password=password)
            login(request, user)
            return redirect('/articles/')

def logout_view(request):
    logout(request)
    return redirect('/user/login/')


def user_data(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        context = {
            'user': user
        }
        return render(request, 'user_profile.html', context)
    except:
        redirect('/')
