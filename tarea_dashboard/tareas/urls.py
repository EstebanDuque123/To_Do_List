from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.lista_tareas, name='lista_tareas'),
    path('crear/', views.crear_tarea, name='crear_tarea'),
    path('editar/<int:tarea_id>/', views.editar_tarea, name='editar_tarea'),
    path('eliminar/<int:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('completar/<int:tarea_id>/', views.completar_tarea, name='completar_tarea'),
    path('registro/', views.registro, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('analisis/', views.analisis, name='analisis'),
]