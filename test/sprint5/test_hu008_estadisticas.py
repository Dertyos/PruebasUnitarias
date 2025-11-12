import pytest
from models import Proyecto, Tarea, Usuario
from datetime import datetime, timedelta

# Casos de Prueba para la Historia de Usuario HU-008: Estadísticas del Proyecto

@pytest.fixture
def setup_proyecto_con_estadisticas():
    proyecto = Proyecto(nombre="Proyecto de Estadísticas")
    usuario1 = Usuario(nombre="Usuario Uno", email="uno@test.com")
    usuario2 = Usuario(nombre="Usuario Dos", email="dos@test.com")

    # Añadir columnas si no existen
    if not any(c.nombre == "Pendiente" for c in proyecto.columnas):
        proyecto.agregar_columna("Pendiente")
    if not any(c.nombre == "En Progreso" for c in proyecto.columnas):
        proyecto.agregar_columna("En Progreso")
    if not any(c.nombre == "Completada" for c in proyecto.columnas):
        proyecto.agregar_columna("Completada")

    tareas = [
        # Tareas Pendientes
        Tarea(titulo="Tarea Pendiente 1", prioridad="Alta", asignado_a=usuario1.usuario_id),
        Tarea(titulo="Tarea Pendiente 2", prioridad="Media"),
        # Tareas En Progreso
        Tarea(titulo="Tarea En Progreso 1", prioridad="Urgente", asignado_a=usuario2.usuario_id),
        # Tareas Completadas
        Tarea(titulo="Tarea Completada 1", prioridad="Baja"),
        Tarea(titulo="Tarea Completada 2", prioridad="Media", asignado_a=usuario1.usuario_id)
    ]

    columna_pendiente = next((c for c in proyecto.columnas if c.nombre == "Pendiente"), None)
    columna_en_progreso = next((c for c in proyecto.columnas if c.nombre == "En Progreso"), None)
    columna_completada = next((c for c in proyecto.columnas if c.nombre == "Completada"), None)

    if columna_pendiente:
        columna_pendiente.agregar_tarea(tareas[0])
        columna_pendiente.agregar_tarea(tareas[1])
    if columna_en_progreso:
        columna_en_progreso.agregar_tarea(tareas[2])
    if columna_completada:
        columna_completada.agregar_tarea(tareas[3])
        columna_completada.agregar_tarea(tareas[4])
        # Simular que las tareas están completadas
        for tarea in [tareas[3], tareas[4]]:
            tarea.estado = "Completada"

    return proyecto

def test_hu008_ca1_total_tareas(setup_proyecto_con_estadisticas):
    """Validar que se muestra el total de tareas del proyecto."""
    proyecto = setup_proyecto_con_estadisticas
    estadisticas = proyecto.obtener_estadisticas()
    assert estadisticas['total_tareas'] == 5

def test_hu008_ca2_conteo_por_estado(setup_proyecto_con_estadisticas):
    """Validar que se muestra el conteo de tareas por estado actual."""
    proyecto = setup_proyecto_con_estadisticas
    estadisticas = proyecto.obtener_estadisticas()
    assert estadisticas['por_estado']['Pendiente'] == 2
    assert estadisticas['por_estado']['En Progreso'] == 1
    assert estadisticas['por_estado']['Completada'] == 2
    assert estadisticas['por_estado'].get('Bloqueada', 0) == 0

def test_hu008_ca4_conteo_por_prioridad(setup_proyecto_con_estadisticas):
    """Validar que se muestra el conteo de tareas por nivel de prioridad."""
    proyecto = setup_proyecto_con_estadisticas
    estadisticas = proyecto.obtener_estadisticas()
    assert estadisticas['por_prioridad']['Urgente'] == 1
    assert estadisticas['por_prioridad']['Alta'] == 1
    assert estadisticas['por_prioridad']['Media'] == 2
    assert estadisticas['por_prioridad']['Baja'] == 1

def test_hu008_ca6_conteo_asignacion(setup_proyecto_con_estadisticas):
    """Validar que se muestra el conteo de tareas asignadas vs sin asignar."""
    proyecto = setup_proyecto_con_estadisticas
    estadisticas = proyecto.obtener_estadisticas()
    assert estadisticas['asignacion']['asignadas'] == 3
    assert estadisticas['asignacion']['sin_asignar'] == 2

def test_hu008_ca8_conteo_por_columna(setup_proyecto_con_estadisticas):
    """Validar que se muestra el conteo de tareas por columna."""
    proyecto = setup_proyecto_con_estadisticas
    estadisticas = proyecto.obtener_estadisticas()
    assert estadisticas['por_columna']['Pendiente'] == 2
    assert estadisticas['por_columna']['En Progreso'] == 1
    assert estadisticas['por_columna']['Completada'] == 2