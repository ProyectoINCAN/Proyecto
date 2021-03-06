"""Proyecto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/', login, {'template_name': 'admin/login.html'}, name="login"),
    url(r'^pacientes/', include('apps.pacientes.urls', namespace="pacientes")),
    url(r'^agendamientos/', include('apps.agendamientos.urls', namespace="agendamientos")),
    url(r'^consultorios/', include('apps.consultorios.urls', namespace="consultorios")),
    url(r'^principal/', include('apps.principal.urls', namespace="principal")),
    url(r'', include('apps.seguridad.urls')),
    url(r'^internaciones/', include('apps.internaciones.urls', namespace="internaciones")),

]

