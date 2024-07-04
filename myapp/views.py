from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile, Experience, Proyecto, Application, Modalidad, Categoria,Message
from .forms import UserProfileForm, ExperienceForm, ContactoForm, CustomUserCreationForm, ProyectoForm, ProyectoSearchForm,ApplicationForm,MessageForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import ApplicationStatusForm


# Páginas generales
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def chat(request):
    return render(request, 'chat.html')

# Perfil de usuario
@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    experiences = Experience.objects.filter(user_profile=user_profile)
    default_avatar = 'static/img/default-avatar.png'

    context = {
        'user_profile': user_profile,
        'experiences': experiences,
        'default_avatar': default_avatar,
    }

    return render(request, 'perfil/profile.html', context)

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Perfil actualizado correctamente")
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'perfil/edit_profile.html', {'profile_form': profile_form, 'experience_form': ExperienceForm()})

@login_required
def add_experience(request, experience_id=None):
    if experience_id:
        experience = get_object_or_404(Experience, id=experience_id, user_profile__user=request.user)
    else:
        experience = Experience(user_profile=request.user.userprofile)

    if request.method == 'POST':
        experience_form = ExperienceForm(request.POST, instance=experience)
        if experience_form.is_valid():
            experience_form.save()
            messages.success(request, "Experiencia actualizada correctamente")
            return redirect('profile')
    else:
        experience_form = ExperienceForm(instance=experience)

    return render(request, 'perfil/edit_experience.html', {'experience_form': experience_form})

# Proyectos
def projects(request):
    form = ProyectoSearchForm(request.GET or None)
    proyectos = Proyecto.objects.all()

    if request.method == 'GET' and form.is_valid():
        nombre = form.cleaned_data.get('nombre')
        modalidad = form.cleaned_data.get('modalidad')
        categoria = form.cleaned_data.get('categoria')
        salario = form.cleaned_data.get('salario')

        if nombre:
            proyectos = proyectos.filter(nombre__icontains=nombre)
        if modalidad:
            proyectos = proyectos.filter(modalidad=modalidad)
        if categoria:
            proyectos = proyectos.filter(categoria=categoria)
        if salario:
            proyectos = proyectos.filter(salario__gte=salario)

    return render(request, 'projects.html', {'proyectos': proyectos, 'form': form})

def project_detail(request, project_id):
    proyecto = get_object_or_404(Proyecto, id=project_id)
    return render(request, 'project_detail.html', {'proyecto': proyecto})

   
# Modulos Gestion de Proyectos
@login_required
def agregar_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.creator = request.user  # Asigna el usuario actual como el creador del proyecto
            proyecto.save()
            messages.success(request, 'El proyecto se ha creado con éxito.')
            return redirect('proyecto_listar')  # Ajusta esta redirección según tus necesidades
    else:
        form = ProyectoForm()
    return render(request, 'projects/agregar.html', {'form': form})

# Modulo gestion de proyectos
def mis_proyectos(request):
    proyectos = Proyecto.objects.filter(creator=request.user)
    modalidades = Modalidad.objects.all()
    categorias = Categoria.objects.all()
    
    if request.method == 'POST':
        print("Solicitud POST recibida")
        if 'edit_project' in request.POST:
            print("Formulario de edición enviado")
            proyecto_id = request.POST.get('proyecto_id')
            print(f"Proyecto ID: {proyecto_id}")
            proyecto = get_object_or_404(Proyecto, id=proyecto_id, creator=request.user)
            form = ProyectoForm(request.POST, request.FILES, instance=proyecto)
            if form.is_valid():
                print("Formulario válido")
                form.save()
                messages.success(request, 'El proyecto ha sido actualizado correctamente.')
                return redirect('mis_proyectos')
            else:
                print("Formulario inválido", form.errors)
                messages.error(request, 'Error al actualizar el proyecto. Verifica los datos ingresados.')
        elif 'delete_project' in request.POST:
            print("Formulario de eliminación enviado")
            proyecto_id = request.POST.get('proyecto_id')
            proyecto = get_object_or_404(Proyecto, id=proyecto_id, creator=request.user)
            proyecto.delete()
            messages.success(request, 'El proyecto ha sido eliminado correctamente.')
            return redirect('mis_proyectos')
    
    proyecto_form = ProyectoForm()
    return render(request, 'projects/mis_proyectos.html', {
        'proyectos': proyectos,
        'proyecto_form': proyecto_form,
        'modalidades': modalidades,
        'categorias': categorias
    })


@login_required
def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id, creator=request.user)
    if request.method == 'POST':
        proyecto.delete()
        messages.success(request, 'El proyecto ha sido eliminado correctamente.')
        return redirect('mis_proyectos')
    return render(request, 'myapp/eliminar_proyecto.html', {'proyecto': proyecto})

# listar?
@login_required
def listar_proyecto(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'projects/listar.html', {'proyectos': proyectos})

# Postulación a proyectos
@login_required
def apply_to_project(request, project_id):
    project = get_object_or_404(Proyecto, id=project_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()

            # Enviar correo al creador del proyecto
            subject = 'Nueva aplicación para tu proyecto'
            message = f'El usuario {request.user.username} ha aplicado a tu proyecto {project.nombre}.'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [project.creator.email]

            try:
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, 'Tu aplicación ha sido enviada con éxito.')
            except Exception as e:
                messages.error(request, f'Error al enviar el correo: {e}')

            return redirect('project_detail', project_id=project.id)
    else:
        form = ApplicationForm(initial={'project': project})

    return render(request, 'projects/apply.html', {'form': form, 'project': project})

# Mis Postulaciones
@login_required
def my_applications(request):
    applications = Application.objects.filter(user=request.user)
    return render(request, 'perfil/my_applications.html', {'applications': applications})

# Administrar Aplicaciones a Proyectos
@login_required
def manage_applications(request):
    projects = Proyecto.objects.filter(creator=request.user)
    applications = Application.objects.filter(project__in=projects)
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST)
        if form.is_valid():
            application_id = form.cleaned_data['application_id']
            status = form.cleaned_data['status']
            application = Application.objects.get(id=application_id)
            application.status = status
            application.save()
            messages.success(request, 'Estado de la aplicación actualizado correctamente.')
            return redirect('manage_applications')
    else:
        form = ApplicationStatusForm()

    context = {
        'projects': projects,
        'applications': applications,
        'form': form
    }

    return render(request, 'projects/manage_applications.html', context)





# Contacto
def contact(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Formulario enviado correctamente")
            return redirect('contact')
    else:
        form = ContactoForm()

    return render(request, 'contact.html', {'form': form})

# Registro
def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/registro.html', {'form': form})


def project_detail(request, project_id):
    proyecto = get_object_or_404(Proyecto, id=project_id)
    return render(request, 'project_detail.html', {'proyecto': proyecto})


# Messages

@login_required
def messages_view(request):
    received_messages = Message.objects.filter(recipient=request.user).order_by('-created_at')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.sender = request.user
            new_message.save()
            return redirect('messages_view')
    else:
        form = MessageForm()
    
    return render(request, 'messages/inbox.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
        'form': form,
    })