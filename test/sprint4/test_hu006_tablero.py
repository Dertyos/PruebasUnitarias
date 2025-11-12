import pytest
from models import Proyecto, Tarea, Usuario, Columna

# Casos de Prueba para la Historia de Usuario HU-006: Visualización del Tablero

@pytest.fixture
def setup_proyecto_para_tablero():
    # Setup de un proyecto con varias columnas y tareas para probar el tablero
    proyecto = Proyecto(nombre="Proyecto para Tablero")
    usuario1 = Usuario(nombre="Alice", email="alice@test.com")
    usuario2 = Usuario(nombre="Bob", email="bob@test.com")

    # Crear columnas personalizadas además de las de por defecto
    proyecto.agregar_columna("En Revisión")

    # Tareas con diferentes prioridades, estados y asignaciones
    tareas = {
        "Pendiente": [
            Tarea(titulo="Diseñar UI", prioridad="Alta", asignado_a=usuario1.usuario_id),
            Tarea(titulo="Definir esquema de BD", prioridad="Urgente")
        ],
        "En Progreso": [
            Tarea(titulo="Desarrollar API", prioridad="Media", asignado_a=usuario2.usuario_id)
        ],
        "En Revisión": [
            Tarea(titulo="Revisar PR #123", prioridad="Alta")
        ],
        "Completada": []
    }

    for nombre_columna, lista_tareas in tareas.items():
        columna = next((c for c in proyecto.columnas if c.nombre == nombre_columna), None)
        assert columna is not None, f"La columna '{nombre_columna}' no se encontró."
        for tarea in lista_tareas:
            columna.agregar_tarea(tarea)
            
    return proyecto, usuario1, usuario2

def test_hu006_ca1_mostrar_columnas(setup_proyecto_para_tablero):
    """Validar que se muestran todas las columnas del proyecto actual."""
    proyecto, _, _ = setup_proyecto_para_tablero
    # La prueba real estaría en el CLI, aquí verificamos que el proyecto las tenga
    nombres_columnas = [c.nombre for c in proyecto.columnas]
    assert "Pendiente" in nombres_columnas
    assert "En Progreso" in nombres_columnas
    assert "En Revisión" in nombres_columnas
    assert "Completada" in nombres_columnas

def test_hu006_ca2_mostrar_tareas_en_columnas(setup_proyecto_para_tablero):
    """Validar que se muestran todas las tareas dentro de cada columna."""
    proyecto, _, _ = setup_proyecto_para_tablero
    columna_pendiente = proyecto.obtener_columna_por_nombre("Pendiente")
    assert len(columna_pendiente.tareas) == 2
    columna_en_progreso = proyecto.obtener_columna_por_nombre("En Progreso")
    assert len(columna_en_progreso.tareas) == 1

def test_hu006_ca5_mostrar_usuario_asignado(setup_proyecto_para_tablero):
    """Validar que se muestra el usuario asignado o 'Sin asignar'"""
    proyecto, usuario1, _ = setup_proyecto_para_tablero
    columna_pendiente = proyecto.obtener_columna_por_nombre("Pendiente")
    tarea_asignada = columna_pendiente.tareas[0]
    tarea_no_asignada = columna_pendiente.tareas[1]
    
    assert tarea_asignada.asignado_a == usuario1.usuario_id
    assert tarea_no_asignada.asignado_a is None

def test_hu006_ca6_mostrar_icono_prioridad(setup_proyecto_para_tablero):
    """Validar que se muestra icono de prioridad."""
    proyecto, _, _ = setup_proyecto_para_tablero
    columna_pendiente = proyecto.obtener_columna_por_nombre("Pendiente")
    # La representación (icono) es parte del CLI, aquí probamos el dato
    assert columna_pendiente.tareas[0].prioridad == "Alta"
    assert columna_pendiente.tareas[1].prioridad == "Urgente"

def test_hu006_ca7_conteo_tareas_en_columna(setup_proyecto_para_tablero):
    """Validar que se muestra el conteo total de tareas en cada columna."""
    proyecto, _, _ = setup_proyecto_para_tablero
    columna_pendiente = proyecto.obtener_columna_por_nombre("Pendiente")
    assert len(columna_pendiente.tareas) == 2
    columna_completada = proyecto.obtener_columna_por_nombre("Completada")
    assert len(columna_completada.tareas) == 0

def test_hu006_ca8_mensaje_columna_vacia(setup_proyecto_para_tablero):
    """Validar que se muestra un mensaje '(vacio)' en columnas sin tareas."""
    proyecto, _, _ = setup_proyecto_para_tablero
    columna_completada = proyecto.obtener_columna_por_nombre("Completada")
    # La prueba real estaría en el CLI, aquí verificamos que no tenga tareas
    assert len(columna_completada.tareas) == 0