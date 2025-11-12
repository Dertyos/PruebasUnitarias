import pytest
from models import Tarea, Proyecto, Usuario, Columna
from datetime import datetime

@pytest.fixture
def setup_proyecto():
    propietario = Usuario(nombre="test_user", email="test@example.com")
    proyecto = Proyecto(nombre="Proyecto Tareas", propietario_id=propietario.usuario_id)
    
    if not proyecto.columnas:
        proyecto.agregar_columna("Pendiente")
        proyecto.agregar_columna("En Progreso")
        proyecto.agregar_columna("Completada")
        
    return proyecto, propietario

def test_crear_tarea_con_titulo_obligatorio(setup_proyecto):
    proyecto, propietario = setup_proyecto
    columna_pendiente = proyecto.obtener_columna_por_nombre("Pendiente")
    
    tarea = Tarea(
        titulo="Tarea CA1",
        descripcion="Detalle inicial",
        prioridad="Media",
        asignado_a=propietario.usuario_id
    )
    
    columna_pendiente.agregar_tarea(tarea)
    
    assert tarea.titulo == "Tarea CA1"
    assert tarea.descripcion == "Detalle inicial"
    assert tarea.prioridad == "Media"
    assert tarea.asignado_a == propietario.usuario_id
    assert tarea in columna_pendiente.tareas

def test_titulo_obligatorio_no_vacio():
    with pytest.raises(ValueError, match="El titulo no puede estar vacio"):
        Tarea(titulo="")

def test_descripcion_opcional(setup_proyecto):
    proyecto, _ = setup_proyecto
    columna_pendiente = proyecto.obtener_columna_por_nombre("Pendiente")
    
    tarea = Tarea(titulo="Tarea CA3")
    columna_pendiente.agregar_tarea(tarea)
    
    assert tarea.descripcion == ""
    assert tarea in columna_pendiente.tareas

def test_seleccionar_prioridad(setup_proyecto):
    proyecto, _ = setup_proyecto
    columna_pendiente = proyecto.obtener_columna_por_nombre("Pendiente")
    
    tarea = Tarea(titulo="Tarea CA4", prioridad="Urgente")
    
    assert tarea.prioridad == "Urgente"

def test_prioridad_por_defecto_media(setup_proyecto):
    proyecto, _ = setup_proyecto
    columna_pendiente = proyecto.obtener_columna_por_nombre("Pendiente")
    
    tarea = Tarea(titulo="Tarea CA5")
    
    assert tarea.prioridad == "Media"

def test_seleccionar_columna_destino(setup_proyecto):
    proyecto, _ = setup_proyecto
    columna_progreso = proyecto.obtener_columna_por_nombre("En Progreso")
    
    tarea = Tarea(titulo="Tarea CA6")
    columna_progreso.agregar_tarea(tarea)
    
    assert tarea in columna_progreso.tareas

def test_asignacion_opcional_usuario(setup_proyecto):
    proyecto, propietario = setup_proyecto
    columna_pendiente = proyecto.obtener_columna_por_nombre("Pendiente")
    
    tarea = Tarea(titulo="Tarea CA7", asignado_a=propietario.usuario_id)
    
    assert tarea.asignado_a == propietario.usuario_id

def test_id_unico_uuid_por_tarea():
    tarea1 = Tarea(titulo="Tarea 1")
    tarea2 = Tarea(titulo="Tarea 2")
    
    assert tarea1.tarea_id != tarea2.tarea_id
    assert isinstance(tarea1.tarea_id, str)

def test_estado_inicial_pendiente():
    tarea = Tarea(titulo="Tarea CA9")
    
    assert tarea.estado == "Pendiente"

def test_fechas_creacion_modificacion_automaticas():
    tarea = Tarea(titulo="Tarea CA10")
    
    assert isinstance(datetime.fromisoformat(tarea.fecha_creacion), datetime)
    assert isinstance(datetime.fromisoformat(tarea.fecha_modificacion), datetime)
    assert tarea.fecha_creacion == tarea.fecha_modificacion

def test_guardado_automatico_y_confirmacion(setup_proyecto, mocker):
    proyecto, _ = setup_proyecto
    columna_pendiente = proyecto.obtener_columna_por_nombre("Pendiente")
    
    tarea = Tarea(titulo="Tarea CA11")
    columna_pendiente.agregar_tarea(tarea)
    
    assert any(t.titulo == "Tarea CA11" for t in columna_pendiente.tareas)