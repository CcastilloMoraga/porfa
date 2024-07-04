from django import forms
from .models import Contacto, Proyecto, UserProfile, Experience, Application,Categoria, Modalidad, Message
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from djmoney.forms.widgets import MoneyWidget

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        exclude = ['usuario']  
        fields = ['username', "first_name", "last_name", "email", "password1", "password2"]



class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'salario', 'descripcion', 'modalidad', 'periodo', 'imagen', 'categoria', 'ciudad']
        widgets = {
            'periodo': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProyectoForm, self).__init__(*args, **kwargs)
        self.fields['ciudad'].required = False
        self.fields['modalidad'].widget.attrs.update({'onchange': 'checkModalidad()'})



class ProyectoSearchForm(forms.Form):
    nombre = forms.CharField(required=False, label='Nombre del Proyecto')
    modalidad = forms.ModelChoiceField(queryset=Modalidad.objects.all(), required=False, label='Modalidad')
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=False, label='Categoría')
    ciudad = forms.CharField(required=False, label='Ciudad') 

        
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    hourly_rate = forms.DecimalField(
        widget=MoneyWidget(
            amount_widget=forms.TextInput(attrs={'placeholder': 'Tarifa por hora'}),
            currency_widget=forms.Select(choices=[
                ('CLP', 'CLP'),
                ('USD', 'USD')
            ])
        )
    )

    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'avatar', 'hourly_rate']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'company', 'location', 'start_date', 'end_date', 'description']



class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['project']
        widgets = {
            'project': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['project'].required = True


class ApplicationStatusForm(forms.ModelForm):
    application_id = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = Application
        fields = ['status']



class MessageForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    
    class Meta:
        model = Message
        fields = ['recipient', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }