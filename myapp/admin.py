from django.contrib import admin
from .models import Proyecto, Categoria, Modalidad, Application, UserProfile, Experience

class ProyectosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'salario', 'descripcion', 'modalidad', 'periodo', 'creator', 'categoria', 'ciudad')
    list_filter = ('modalidad', 'periodo', 'categoria', 'creator')  # Asegúrate de usar 'creator' en lugar de 'usuario'

admin.site.register(Proyecto, ProyectosAdmin)
admin.site.register(Categoria)
admin.site.register(Modalidad)
admin.site.register(Application)
admin.site.register(UserProfile)
admin.site.register(Experience)
