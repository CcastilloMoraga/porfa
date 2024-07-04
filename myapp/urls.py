from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/experience/add/', views.add_experience, name='add_experience'),

    path('projects/', views.projects, name='projects'),
    path('projects/agregar/', views.agregar_proyecto, name='agregar_proyecto'),

    path('projects/apply/<int:project_id>/', views.apply_to_project, name='apply_to_project'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),

  
    path('contact/', views.contact, name='contact'),
    
    path('registro/', views.registro, name='registro'),

    path('profile/applications/', views.my_applications, name='my_applications'),

    path('projects/manage_applications/', views.manage_applications, name='manage_applications'),
    path('messages/', views.messages_view, name='messages_view'),

    #R
    path('projects/listar/', views.listar_proyecto, name='proyecto_listar'),

    path('projects/mis_proyectos/', views.mis_proyectos, name='mis_proyectos'),
    path('eliminar_proyecto/<int:proyecto_id>/', views.eliminar_proyecto, name='eliminar_proyecto'),
]