import pytest
from models import Tarea, Proyecto, Usuario, Columna
from datetime import datetime

@pytest.fixture
def setup_proyecto_con_tarea():
    propietario = Usuario(nombre="test_user", email="test@example.com")
    proyecto = Proyecto(nombre="Proyecto Edicion", propietario_id=propietario.usuario_id)
    
    columna_pendiente = next((col for col in proyecto.columnas if col.nombre == "Pendiente"), None)
    assert columna_pendiente is not None, "La columna 'Pendiente' no se creó por defecto"

    tarea = Tarea(titulo="Tarea a Editar", descripcion="Descripción original")
    columna_pendiente.agregar_tarea(tarea)
    
    return proyecto, tarea, propietario

def test_cambiar_titulo_tarea(setup_proyecto_con_tarea):
    _, tarea, _ = setup_proyecto_con_tarea
    
    nuevo_titulo = "Título Actualizado"
    tarea.actualizar(titulo=nuevo_titulo)
    
    assert tarea.titulo == nuevo_titulo

def test_cambiar_descripcion_tarea(setup_proyecto_con_tarea):
    _, tarea, _ = setup_proyecto_con_tarea
    
    nueva_descripcion = "Descripción actualizada"
    tarea.actualizar(descripcion=nueva_descripcion)
    
    assert tarea.descripcion == nueva_descripcion

def test_cambiar_prioridad_tarea(setup_proyecto_con_tarea):
    _, tarea, _ = setup_proyecto_con_tarea
    
    nueva_prioridad = "Urgente"
    tarea.actualizar(prioridad=nueva_prioridad)
    
    assert tarea.prioridad == nueva_prioridad

def test_cambiar_estado_tarea(setup_proyecto_con_tarea):
    _, tarea, _ = setup_proyecto_con_tarea
    
    nuevo_estado = "En Progreso"
    tarea.actualizar(estado=nuevo_estado)
    
    assert tarea.estado == nuevo_estado

def test_cambiar_usuario_asignado(setup_proyecto_con_tarea):
    _, tarea, propietario = setup_proyecto_con_tarea
    otro_usuario = Usuario(nombre="otro_user", email="otro@example.com")
    
    tarea.actualizar(asignado_a=otro_usuario.usuario_id)
    
    assert tarea.asignado_a == otro_usuario.usuario_id

def test_mover_tarea_a_otra_columna(setup_proyecto_con_tarea):
    proyecto, tarea, _ = setup_proyecto_con_tarea
    columna_pendiente = proyecto.obtener_columna_por_nombre("Pendiente")
    
    proyecto.agregar_columna("Completada")
    columna_completada = proyecto.obtener_columna_por_nombre("Completada")
    
    columna_pendiente.eliminar_tarea(tarea.tarea_id)
    columna_completada.agregar_tarea(tarea)
    
    assert tarea not in columna_pendiente.tareas
    assert tarea in columna_completada.tareas

def test_agregar_etiquetas(setup_proyecto_con_tarea):
    _, tarea, _ = setup_proyecto_con_tarea
    
    tarea.agregar_etiqueta("backend")
    tarea.agregar_etiqueta("urgente")
    
    assert "backend" in tarea.etiquetas
    assert "urgente" in tarea.etiquetas

def test_eliminar_etiquetas_existentes(setup_proyecto_con_tarea):
    _, tarea, _ = setup_proyecto_con_tarea
    tarea.agregar_etiqueta("backend")
    
    tarea.eliminar_etiqueta("backend")
    
    assert "backend" not in tarea.etiquetas

def test_ver_detalles_completos_tarea(setup_proyecto_con_tarea):
    _, tarea, propietario = setup_proyecto_con_tarea
    
    assert tarea.titulo == "Tarea a Editar"
    assert tarea.descripcion == "Descripción original"
    assert tarea.prioridad == "Media"
    assert tarea.estado == "Pendiente"
    assert isinstance(datetime.fromisoformat(tarea.fecha_creacion), datetime)

def test_eliminar_tarea_con_confirmacion(setup_proyecto_con_tarea):
    proyecto, tarea, _ = setup_proyecto_con_tarea
    columna_pendiente = proyecto.obtener_columna_por_nombre("Pendiente")
    
    columna_pendiente.eliminar_tarea(tarea.tarea_id)
    
    assert tarea not in columna_pendiente.tareas

def test_fecha_modificacion_automatica(setup_proyecto_con_tarea):
    _, tarea, _ = setup_proyecto_con_tarea
    fecha_modificacion_inicial = tarea.fecha_modificacion
    
    tarea.actualizar(titulo="Nuevo Título para Fecha")
    
    assert tarea.fecha_modificacion != fecha_modificacion_inicial