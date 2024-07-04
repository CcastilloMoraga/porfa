from django.db import models
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField
from decimal import Decimal, InvalidOperation
from django import forms


# Modelos
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    hourly_rate = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.user.username

class Experience(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

class Modalidad(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre



class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre




class Proyecto(models.Model):
    nombre = models.CharField(max_length=50)
    salario = models.IntegerField(default=0)
    descripcion = models.TextField()
    modalidad = models.ForeignKey('Modalidad', on_delete=models.PROTECT)
    periodo = models.DateField()
    imagen = models.ImageField(upload_to="proyectos", null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)  # Cambiado de usuario a creator
    categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT, null=True, blank=True)
    ciudad = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nombre

    def salario_formateado(self):
        return f"{self.salario:,}".replace(",", ".")

    @property
    def imagen_url(self):
        if self.imagen and hasattr(self.imagen, 'url'):
            return self.imagen.url
        return '/static/img/default-image.png'


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
    ]

    project = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_applied = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'{self.user.username} - {self.project.nombre}'





# Contacto
opciones_consultas = [
    [0, "Consulta"],
    [1, "Reclamo"],
    [2, "Sugerencia"],
    [3, "Felicitaciones"]
] 

class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    tipo_consulta = models.IntegerField(choices=opciones_consultas)
    mensaje = models.TextField()
    avisos = models.BooleanField()

    def __str__(self):
        return self.nombre
    


#Mensajes
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} to {self.recipient.username}'