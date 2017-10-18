from django.conf.urls import url

from apps.principal import views

urlpatterns = [
    url(r'^distrito/(?P<id_departamento>\d+)$', views.distrito, name='distrito'),
    url(r'^distrito/([\w\s-]+)/$',  views.distritoByDepartamento, name='distritos'),
    url(r'^nacionalidad/(?P<nacionalidad_id>\d+)$', views.nacionalidad, name='nacionalidad'),
    url(r'^departamento/(?P<pais_codigo>[\w\-]+)/$', views.departamento, name='departamento'),
    url(r'^barrio/(?P<id_distrito>\d+)$', views.barrio, name='barrio'),

    url(r'^usuarios/crear/$', views.UsuarioCreateView.as_view(), name='usuario_nuevo'),
    url(r'^usuarios/$', views.UsuarioList.as_view(), name='user_list_global'),
    url(r'^usuarios/(?P<user_id>\d+)/editar/$', views.user_update_view, name='user_update_global'),

    url(r'^usuarios/(?P<user_id>\d+)/eliminar/$', views.UserDeleteView.as_view(), name='user_delete_global'),
    url(r'^usuarios/(?P<user_id>\d+)/editar/cambiar-pass/$', views.UserUpdatePasswordView.as_view(),
        name='user_update_pass_global'),

]