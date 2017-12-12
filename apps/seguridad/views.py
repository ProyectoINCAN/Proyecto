from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from apps.consultorios.models import Medico


def login_view(request):
    if request.user.is_authenticated():
        return redirect(reverse("principal:index"))

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #luego se definira el redirect al dashboard correspondiente de acuerdo al tipo
                #de usuario logueado.
                if Medico.objects.filter(usuario=user).exists():
                    return redirect('consultorios:dashboard_medico')
                else:
                    return redirect('principal:index')
            else:
                return render(request, "principal/login.html", {'error': 'Cuenta inactiva'})
        else:
            return render(request, "principal/login.html", {'error': 'Usuario y/o Contraseña inválidos.'})

    return render(request, "principal/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
