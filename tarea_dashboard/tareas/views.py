from .models import Tarea
from .forms import TareaForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import RegistroForm
from django.shortcuts import render, get_object_or_404, redirect

@login_required
def lista_tareas(request):
    filtro = request.GET.get("filtro", "todas")  # por defecto "todas"

    # Tareas filtradas por usuario
    tareas_usuario = Tarea.objects.filter(usuario=request.user)

    # Contadores
    total_tareas = tareas_usuario.count()
    pendientes_count = tareas_usuario.filter(completada=False).count()
    completadas_count = tareas_usuario.filter(completada=True).count()

    # Filtrar según el parámetro
    if filtro == "completadas":
        tareas = tareas_usuario.filter(completada=True).order_by('-fecha_creacion')
    elif filtro == "pendientes":
        tareas = tareas_usuario.filter(completada=False).order_by('-fecha_creacion')
    else:
        tareas = tareas_usuario.order_by('-fecha_creacion')

    return render(request, 'tareas/lista_tareas.html', {
        'tareas': tareas,
        'filtro': filtro,
        'total_tareas': total_tareas,
        'pendientes_count': pendientes_count,
        'completadas_count': completadas_count,
    })

@login_required
def crear_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.usuario = request.user
            tarea.save()
            return redirect('lista_tareas')
    else:
        form = TareaForm()
    return render(request, 'tareas/crear_tarea.html', {'form': form})


@login_required
def editar_tarea(request, tarea_id):
    tarea = Tarea.objects.get(id=tarea_id, usuario=request.user)
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('lista_tareas')
    else:
        form = TareaForm(instance=tarea)
    return render(request, 'tareas/formulario_tarea.html', {'form': form})


@login_required
def completar_tarea(request, tarea_id):
    tarea = Tarea.objects.get(id=tarea_id, usuario=request.user)
    tarea.completada = True
    tarea.fecha_completado = timezone.now()
    tarea.save()
    return redirect('lista_tareas')

@login_required
def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id, usuario=request.user)
    if request.method == 'POST':
        tarea.delete()
        return redirect('lista_tareas')
    return render(request, 'tareas/confirmar_eliminar.html', {'tarea': tarea})

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirigir al login
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def analisis(request):
    tareas = Tarea.objects.filter(usuario=request.user)
    total = tareas.count()
    completadas = tareas.filter(completada=True).count()
    pendientes = tareas.filter(completada=False).count()

    context = {
        'total': total,
        'completadas': completadas,
        'pendientes': pendientes,
        'datos': [completadas, pendientes]
    }
    return render(request, 'tareas/analisis.html', context)