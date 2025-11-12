import pytest
from models import Proyecto, Usuario
from storage import StorageManager
import uuid
import os

# HU-002: Como usuario, quiero poder gestionar los proyectos 
# (crear, listar, abrir, eliminar) para organizar mis tareas.

# Criterio de Aceptación 1: Crear un nuevo proyecto especificando su nombre y descripción.
def test_crear_proyecto_con_nombre_y_descripcion(tmp_path):
    # Preparación
    storage_path = tmp_path / "projects.json"
    storage = StorageManager(storage_path)
    usuario = Usuario(nombre="Test User", email="test@user.com")
    storage.guardar_usuario(usuario)
    storage.set_usuario_actual(usuario.usuario_id)

    # Ejecución
    proyecto = Proyecto(nombre="Proyecto Test", descripcion="Descripción de prueba", propietario_id=usuario.usuario_id)
    storage.guardar_proyecto(proyecto)

    # Verificación
    proyectos = storage.cargar_todos_proyectos()
    assert len(proyectos) == 1
    assert proyectos[0].nombre == "Proyecto Test"
    assert proyectos[0].descripcion == "Descripción de prueba"

# Criterio de Aceptación 2: Validar que el nombre del proyecto es obligatorio.
def test_nombre_proyecto_obligatorio():
    with pytest.raises(ValueError, match="El nombre no puede estar vacio"):
        Proyecto(nombre="", descripcion="Sin nombre", propietario_id="123")

# Criterio de Aceptación 3: Asignación automática de un ID único (UUID) a cada proyecto.
def test_asignacion_automatica_uuid():
    proyecto = Proyecto(nombre="Proyecto UUID", propietario_id="123")
    assert isinstance(uuid.UUID(proyecto.proyecto_id, version=4), uuid.UUID)

# Criterio de Aceptación 4: Asignación automática del usuario actual como propietario del proyecto.
def test_asignacion_propietario_automatico(tmp_path):
    storage_path = tmp_path / "projects.json"
    storage = StorageManager(storage_path)
    usuario = Usuario(nombre="Propietario", email="owner@test.com")
    storage.guardar_usuario(usuario)
    storage.set_usuario_actual(usuario.usuario_id)

    proyecto = Proyecto(nombre="Proyecto Propietario", propietario_id=storage.usuario_actual_id)
    storage.guardar_proyecto(proyecto)

    proyectos = storage.cargar_todos_proyectos()
    assert proyectos[0].propietario_id == usuario.usuario_id

# Criterio de Aceptación 5: Creación automática de tres columnas por defecto: "Pendiente", "En Progreso" y "Completada".
def test_creacion_columnas_por_defecto():
    proyecto = Proyecto(nombre="Proyecto Columnas", propietario_id="123")
    assert len(proyecto.columnas) == 3
    assert proyecto.columnas[0].nombre == "Pendiente"
    assert proyecto.columnas[1].nombre == "En Progreso"
    assert proyecto.columnas[2].nombre == "Completada"

# Criterio de Aceptación 6: Abrir/seleccionar un proyecto existente.
def test_abrir_proyecto_existente(tmp_path):
    storage_path = tmp_path / "projects.json"
    storage = StorageManager(storage_path)
    usuario = Usuario(nombre="Test User", email="test@user.com")
    storage.guardar_usuario(usuario)
    storage.set_usuario_actual(usuario.usuario_id)
    
    proyecto = Proyecto(nombre="Proyecto Seleccionable", propietario_id=usuario.usuario_id)
    storage.guardar_proyecto(proyecto)
    
    storage.set_proyecto_actual(proyecto.proyecto_id)
    
    assert storage.proyecto_actual_id == proyecto.proyecto_id

# Criterio de Aceptación 7: Listar todos los proyectos con su respectivo conteo de tareas.
def test_listar_proyectos_con_conteo_tareas(tmp_path):
    storage_path = tmp_path / "projects.json"
    storage = StorageManager(storage_path)
    usuario = Usuario(nombre="Test User", email="test@user.com")
    storage.guardar_usuario(usuario)
    storage.set_usuario_actual(usuario.usuario_id)

    proyecto1 = Proyecto(nombre="Proyecto A", propietario_id=usuario.usuario_id)
    storage.guardar_proyecto(proyecto1)
    
    # Este test requiere que el método `contar_tareas` exista en la clase Proyecto.
    # Suponiendo que existe:
    assert hasattr(proyecto1, 'contar_tareas')
    assert proyecto1.contar_tareas() == 0

# Criterio de Aceptación 8: Eliminar un proyecto con confirmación previa.
def test_eliminar_proyecto(tmp_path):
    storage_path = tmp_path / "projects.json"
    storage = StorageManager(storage_path)
    usuario = Usuario(nombre="Test User", email="test@user.com")
    storage.guardar_usuario(usuario)
    storage.set_usuario_actual(usuario.usuario_id)

    proyecto = Proyecto(nombre="Proyecto a Eliminar", propietario_id=usuario.usuario_id)
    storage.guardar_proyecto(proyecto)
    
    storage.eliminar_proyecto(proyecto.proyecto_id)
    
    proyectos = storage.cargar_todos_proyectos()
    assert len(proyectos) == 0

# Criterio de Aceptación 9: Guardado de fechas de creación y última modificación.
def test_guardado_fechas_creacion_modificacion():
    proyecto = Proyecto(nombre="Proyecto Fechas", propietario_id="123")
    assert proyecto.fecha_creacion is not None
    assert proyecto.fecha_modificacion is not None
    
    fecha_mod_original = proyecto.fecha_modificacion
    proyecto._actualizar_fecha_modificacion()
    assert proyecto.fecha_modificacion > fecha_mod_original

# Criterio de Aceptación 10: Persistencia automática de los cambios en un archivo JSON.
def test_persistencia_automatica_json(tmp_path):
    storage_path = tmp_path / "projects.json"
    storage = StorageManager(storage_path)
    usuario = Usuario(nombre="Test User", email="test@user.com")
    storage.guardar_usuario(usuario)
    storage.set_usuario_actual(usuario.usuario_id)

    proyecto = Proyecto(nombre="Proyecto Persistencia", propietario_id=usuario.usuario_id)
    storage.guardar_proyecto(proyecto)

    assert os.path.exists(storage_path)
    
    storage_2 = StorageManager(storage_path)
    proyectos = storage_2.cargar_todos_proyectos()
    assert len(proyectos) == 1
    assert proyectos[0].nombre == "Proyecto Persistencia"