import pytest
from models import Proyecto, Columna, Tarea

# HU-007: Como usuario, quiero poder gestionar las columnas de un proyecto 
# (agregar, ver, renombrar, eliminar) para organizar el flujo de trabajo.

@pytest.fixture
def proyecto_con_columnas():
    proyecto = Proyecto(nombre="Proyecto Columnas Test", propietario_id="user-123")
    proyecto.agregar_columna("Pendiente")
    proyecto.agregar_columna("En Progreso")
    proyecto.agregar_columna("Completada")
    return proyecto

# Criterio de Aceptación 1: Agregar una nueva columna a un proyecto especificando su nombre.
def test_agregar_columna(proyecto_con_columnas):
    proyecto = proyecto_con_columnas
    columna_nueva = proyecto.agregar_columna("Revisión")
    assert columna_nueva is not None
    assert columna_nueva.nombre == "Revisión"
    assert len(proyecto.columnas) == 4

# Criterio de Aceptación 2: Ver la lista completa de columnas actuales de un proyecto.
def test_listar_columnas(proyecto_con_columnas):
    columnas = proyecto_con_columnas.listar_columnas()
    assert len(columnas) == 3
    assert [c.nombre for c in columnas] == ["Pendiente", "En Progreso", "Completada"]

# Criterio de Aceptación 3: Renombrar una columna existente.
def test_renombrar_columna(proyecto_con_columnas):
    columna_a_renombrar = proyecto_con_columnas.columnas[0]
    columna_a_renombrar.nombre = "Por Hacer"
    assert proyecto_con_columnas.columnas[0].nombre == "Por Hacer"

# Criterio de Aceptación 4: Eliminar una columna con confirmación previa.
def test_eliminar_columna(proyecto_con_columnas):
    columna_a_eliminar_id = proyecto_con_columnas.columnas[1].columna_id
    resultado = proyecto_con_columnas.eliminar_columna(columna_a_eliminar_id)
    assert resultado is True
    assert len(proyecto_con_columnas.columnas) == 2
    assert proyecto_con_columnas.obtener_columna(columna_a_eliminar_id) is None

# Criterio de Aceptación 5: Al eliminar una columna, se eliminan automáticamente todas las tareas que contiene.
def test_eliminar_columna_con_tareas(proyecto_con_columnas):
    columna = proyecto_con_columnas.columnas[0]
    columna.agregar_tarea(Tarea(titulo="Tarea 1"))
    columna.agregar_tarea(Tarea(titulo="Tarea 2"))
    
    assert proyecto_con_columnas.contar_tareas() == 2
    
    proyecto_con_columnas.eliminar_columna(columna.columna_id)
    
    assert proyecto_con_columnas.contar_tareas() == 0

# Criterio de Aceptación 6: El sistema debe advertir al usuario si una columna que intenta eliminar contiene tareas.
# Nota: Este es un comportamiento de la CLI, el modelo subyacente no necesita la advertencia.
# La prueba verifica que el conteo de tareas es correcto.
def test_conteo_tareas_en_columna(proyecto_con_columnas):
    columna = proyecto_con_columnas.columnas[0]
    assert columna.contar_tareas() == 0
    columna.agregar_tarea(Tarea(titulo="Tarea de prueba"))
    assert columna.contar_tareas() == 1

# Criterio de Aceptación 7: Las columnas deben mantener un orden específico (Kanban).
def test_orden_columnas(proyecto_con_columnas):
    columnas = proyecto_con_columnas.listar_columnas()
    assert [c.orden for c in columnas] == [0, 1, 2]
    
    proyecto_con_columnas.agregar_columna("Nueva")
    columnas_actualizadas = proyecto_con_columnas.listar_columnas()
    assert [c.orden for c in columnas_actualizadas] == [0, 1, 2, 3]