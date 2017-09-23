from django.conf.urls import url

from apps.principal import views

urlpatterns = [
    url(r'^distrito/(?P<id_departamento>\d+)$', views.distrito, name='distrito'),
    url(r'^distrito/(?P<departamento>\w{1,50})/$',  views.distritoByDepartamento, name='distritos'),
    url(r'^nacionalidad/(?P<nacionalidad_id>\d+)$', views.nacionalidad, name='nacionalidad'),
    url(r'^departamento/(?P<pais_codigo>[\w\-]+)/$', views.departamento, name='departamento'),

]