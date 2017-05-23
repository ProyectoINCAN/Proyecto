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

from apps.agendamientos.views import prueba

urlpatterns = [
    url(r'^', admin.site.urls),
    url(r'^pacientes/', include('apps.pacientes.urls', namespace="pacientes")),
    url(r'^agendamientos/', include('apps.agendamientos.urls', namespace="agendamientos")),
    url(r'^consultorios/', include('apps.consultorios.urls', namespace="consultorios")),
    url(r'^prueba/', prueba),
    url(r'^select2/', include('django_select2.urls')),

]

