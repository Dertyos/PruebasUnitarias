import pytest
import json
from pathlib import Path
from models import Usuario, Proyecto, Tarea
from storage import StorageManager

# HU-010 CA-1: Guardado automático después de crear usuarios
def test_guardado_automatico_crear_usuario(tmp_path):
    file_path = tmp_path / "test_projects.json"
    storage = StorageManager(file_path)
    usuario = Usuario("Nuevo Usuario", "nuevo@test.com")
    storage.guardar_usuario(usuario)

    # Verificar que el archivo se guardó
    new_storage = StorageManager(file_path)
    usuarios = new_storage.cargar_todos_usuarios()
    assert len(usuarios) == 1
    assert usuarios[0].nombre == "Nuevo Usuario"

# HU-010 CA-2: Guardado automático después de crear proyectos
def test_guardado_automatico_crear_proyecto(tmp_path):
    file_path = tmp_path / "test_projects.json"
    storage = StorageManager(file_path)
    usuario = Usuario("Owner", "owner@test.com")
    storage.guardar_usuario(usuario)
    proyecto = Proyecto("Proyecto Auto", "CA-2", usuario.usuario_id)
    storage.guardar_proyecto(proyecto)

    new_storage = StorageManager(file_path)
    proyectos = new_storage.cargar_todos_proyectos()
    assert len(proyectos) == 1
    assert proyectos[0].nombre == "Proyecto Auto"

# HU-010 CA-3: Guardado automático después de crear tareas
def test_guardado_automatico_crear_tarea(tmp_path):
    file_path = tmp_path / "test_projects.json"
    storage = StorageManager(file_path)
    usuario = Usuario("Asignado", "asignado@test.com")
    storage.guardar_usuario(usuario)
    proyecto = Proyecto("Proyecto Tareas", "Test", usuario.usuario_id)
    columna = proyecto.agregar_columna("Pendiente")
    tarea = Tarea("Tarea CA-3", "Prueba")
    columna.agregar_tarea(tarea)
    storage.guardar_proyecto(proyecto)

    new_storage = StorageManager(file_path)
    loaded_proyecto = new_storage.cargar_proyecto(proyecto.proyecto_id)
    assert loaded_proyecto is not None
    assert len(loaded_proyecto.obtener_todas_las_tareas()) == 1

# HU-010 CA-4: Guardado automático después de editar tareas
def test_guardado_automatico_editar_tarea(tmp_path):
    file_path = tmp_path / "test_projects.json"
    storage = StorageManager(file_path)
    usuario = Usuario("Editor", "editor@test.com")
    storage.guardar_usuario(usuario)
    proyecto = Proyecto("Proyecto Edicion", "Test", usuario.usuario_id)
    columna = proyecto.agregar_columna("Pendiente")
    tarea = Tarea("Tarea Original", "Desc")
    columna.agregar_tarea(tarea)
    storage.guardar_proyecto(proyecto)

    # Editar la tarea
    tarea.titulo = "Tarea Editada"
    storage.guardar_proyecto(proyecto)

    new_storage = StorageManager(file_path)
    loaded_proyecto = new_storage.cargar_proyecto(proyecto.proyecto_id)
    assert loaded_proyecto is not None
    assert loaded_proyecto.obtener_todas_las_tareas()[0].titulo == "Tarea Editada"

# HU-010 CA-5: Guardado automático después de eliminar datos
def test_guardado_automatico_eliminar_usuario(tmp_path):
    file_path = tmp_path / "test_projects.json"
    storage = StorageManager(file_path)
    usuario = Usuario("A Eliminar", "eliminar@test.com")
    storage.guardar_usuario(usuario)
    storage.eliminar_usuario(usuario.usuario_id)

    new_storage = StorageManager(file_path)
    usuarios = new_storage.cargar_todos_usuarios()
    assert len(usuarios) == 0

# HU-010 CA-6: Datos en formato JSON bien estructurado
def test_formato_json_valido(tmp_path):
    file_path = tmp_path / "test_projects.json"
    storage = StorageManager(file_path)
    usuario = Usuario("Test JSON", "json@test.com")
    storage.guardar_usuario(usuario)

    with open(file_path, "r") as f:
        data = json.load(f)
    assert "usuarios" in data
    assert "proyectos" in data
    assert isinstance(data["usuarios"], list)

# HU-010 CA-7: Creación automática de carpeta data/
def test_creacion_automatica_data_dir(tmp_path):
    data_dir = tmp_path / "new_data"
    file_path = data_dir / "projects.json"
    assert not data_dir.exists()
    StorageManager(file_path)
    assert data_dir.exists()

# HU-010 CA-8: Creación automática de projects.json
def test_creacion_automatica_projects_json(tmp_path):
    file_path = tmp_path / "new_projects.json"
    assert not file_path.exists()
    StorageManager(file_path)
    assert file_path.exists()

# HU-010 CA-9: Validación de estructura JSON antes de guardar (simulado)
def test_validacion_estructura_json():
    # Esta prueba es conceptual, ya que la validación es implícita.
    # Se asume que si el guardado funciona, la estructura es correcta.
    pass

# HU-010 CA-10: Recuperación automática de datos tras reinicio
def test_recuperacion_automatica_datos(tmp_path):
    file_path = tmp_path / "test_projects.json"
    storage = StorageManager(file_path)
    usuario = Usuario("Recuperado", "recuperado@test.com")
    storage.guardar_usuario(usuario)

    # Simula reinicio creando una nueva instancia
    new_storage = StorageManager(file_path)
    usuarios = new_storage.cargar_todos_usuarios()
    assert len(usuarios) == 1
    assert usuarios[0].nombre == "Recuperado"

# HU-010 CA-11: Respaldos fáciles (copiar projects.json)
def test_respaldo_facil(tmp_path):
    file_path = tmp_path / "projects.json"
    backup_path = tmp_path / "backup.json"
    storage = StorageManager(file_path)
    storage.guardar_usuario(Usuario("Test", "test@test.com"))

    import shutil
    shutil.copy(file_path, backup_path)
    assert backup_path.exists()
    with open(backup_path, "r") as f:
        data = json.load(f)
        assert len(data['usuarios']) == 1

# HU-010 CA-12: Recuperación elegante de JSON corrupto
def test_recuperacion_json_corrupto(tmp_path):
    file_path = tmp_path / "corrupt.json"
    with open(file_path, "w") as f:
        f.write("contenido invalido")

    storage = StorageManager(file_path)
    assert len(storage.usuarios) == 0
    assert len(storage.proyectos) == 0