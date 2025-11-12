import builtins
import pytest

# Pruebas de Sprint 3 - HU-004: Editar Tarea (CLI)
# Nos guiamos por sprint3Cases.json y Historias de usuario.md

from models import Proyecto, Tarea
import cli as cli_module


class DummyStorage:
    """Stub de StorageManager para evitar dependencias de disco y capturar guardados"""

    def __init__(self, *args, **kwargs):
        self.saved_projects = []

    def guardar_proyecto(self, proyecto):
        self.saved_projects.append(proyecto)
        return True


@pytest.fixture
def cli(monkeypatch):
    # Stub del StorageManager del módulo CLI
    monkeypatch.setattr(cli_module, "StorageManager", DummyStorage)
    monkeypatch.setattr(cli_module.os, "system", lambda *args, **kwargs: 0)

    interfaz = cli_module.CliInterface()
    interfaz.proyecto_actual = Proyecto("Proyecto Sprint3", propietario_id="owner-1")
    col_p = interfaz.proyecto_actual.agregar_columna("Pendiente")
    interfaz.proyecto_actual.agregar_columna("En Progreso")
    interfaz.proyecto_actual.agregar_columna("Completada")
    # Tarea base para edición
    tarea = Tarea("Editar Base", "Desc inicial")
    col_p.agregar_tarea(tarea)
    return interfaz


def feed_inputs(monkeypatch, values):
    it = iter(values)
    monkeypatch.setattr(builtins, "input", lambda prompt=None: next(it))


def obtener_tarea_y_columna(cli):
    col = cli.proyecto_actual.listar_columnas()[0]
    tarea = col.tareas[0]
    return col, tarea


# HU-004 CA-1: Cambiar título de la tarea
def test_hu004_ca1_cambiar_titulo(cli, monkeypatch, capsys):
    columna, tarea = obtener_tarea_y_columna(cli)
    feed_inputs(monkeypatch, ["1", "Editar CA1 Renombrada", "0"])  # Cambiar titulo y guardar
    cli.editar_tarea(columna, tarea)
    out = capsys.readouterr().out
    assert "EDITAR TAREA" in out
    assert "Cambios guardados" in out
    assert tarea.titulo == "Editar CA1 Renombrada"


# HU-004 CA-2: Cambiar descripción
def test_hu004_ca2_cambiar_descripcion(cli, monkeypatch, capsys):
    columna, tarea = obtener_tarea_y_columna(cli)
    feed_inputs(monkeypatch, ["2", "Descripción actualizada", "0"])  # Cambiar descripción
    cli.editar_tarea(columna, tarea)
    out = capsys.readouterr().out
    assert "Cambios guardados" in out
    assert tarea.descripcion == "Descripción actualizada"


# HU-004 CA-3: Cambiar prioridad
def test_hu004_ca3_cambiar_prioridad(cli, monkeypatch, capsys):
    columna, tarea = obtener_tarea_y_columna(cli)
    feed_inputs(monkeypatch, ["3", "4", "0"])  # Prioridad Urgente
    cli.editar_tarea(columna, tarea)
    out = capsys.readouterr().out
    assert "Prioridades:" in out
    assert tarea.prioridad == "Urgente"


# HU-004 CA-4: Cambiar estado
def test_hu004_ca4_cambiar_estado(cli, monkeypatch, capsys):
    columna, tarea = obtener_tarea_y_columna(cli)
    feed_inputs(monkeypatch, ["4", "2", "0"])  # En Progreso
    cli.editar_tarea(columna, tarea)
    out = capsys.readouterr().out
    assert "Estados:" in out
    assert tarea.estado == cli_module.TASK_STATUS_IN_PROGRESS


# HU-004 CA-5: Cambiar usuario asignado
def test_hu004_ca5_cambiar_usuario_asignado(cli, monkeypatch, capsys):
    columna, tarea = obtener_tarea_y_columna(cli)
    feed_inputs(monkeypatch, ["5", "Jeferson", "0"])  # Asignar usuario
    cli.editar_tarea(columna, tarea)
    out = capsys.readouterr().out
    assert "Cambios guardados" in out
    assert tarea.asignado_a == "Jeferson"


# HU-004 CA-6: Mover tarea a otra columna
def test_hu004_ca6_mover_tarea_a_otra_columna(cli, monkeypatch, capsys):
    columna, tarea = obtener_tarea_y_columna(cli)
    feed_inputs(monkeypatch, ["6", "3", "0"])  # Mover a Completada
    cli.editar_tarea(columna, tarea)
    out = capsys.readouterr().out
    assert "Columnas disponibles:" in out
    assert "Tarea movida" in out
    # Verificar que ya no está en Pendiente
    col_pend = cli.proyecto_actual.listar_columnas()[0]
    assert tarea not in col_pend.tareas
    # Verificar que está en Completada
    col_comp = cli.proyecto_actual.listar_columnas()[2]
    assert tarea in col_comp.tareas


# HU-004 CA-7: Agregar etiquetas
def test_hu004_ca7_agregar_etiquetas(cli, monkeypatch, capsys):
    columna, tarea = obtener_tarea_y_columna(cli)
    feed_inputs(monkeypatch, ["7", "backend", "8", "0"])  # Agregar etiqueta y ver detalles
    cli.editar_tarea(columna, tarea)
    out = capsys.readouterr().out
    assert "Etiqueta agregada" in out
    assert "Etiquetas: backend" in out


# HU-004 CA-8: Eliminar etiquetas - funcionalidad no disponible actualmente
def test_hu004_ca8_eliminar_etiquetas_no_disponible(cli, monkeypatch, capsys):
    columna, tarea = obtener_tarea_y_columna(cli)
    # Mostrar menú y validar que no existe opción de eliminar etiqueta
    feed_inputs(monkeypatch, ["8", "0"])  # Solo ver detalles y salir
    cli.editar_tarea(columna, tarea)
    out = capsys.readouterr().out
    # El menú no contiene una opción para eliminar etiquetas
    assert "Eliminar etiqueta" not in out


# HU-004 CA-9: Ver detalles completos de la tarea
def test_hu004_ca9_ver_detalles_completos(cli, monkeypatch, capsys):
    columna, tarea = obtener_tarea_y_columna(cli)
    feed_inputs(monkeypatch, ["8", "0"])  # Ver detalles
    cli.editar_tarea(columna, tarea)
    out = capsys.readouterr().out
    assert "ID: " in out
    assert "Titulo: " in out
    assert "Descripcion: " in out
    assert "Prioridad: " in out
    assert "Estado: " in out
    assert "Asignado a: " in out
    assert "Etiquetas: " in out
    assert "Creada: " in out
    assert "Modificada: " in out


# HU-004 CA-10: Eliminar tarea con confirmación
def test_hu004_ca10_eliminar_tarea_con_confirmacion(cli, monkeypatch, capsys):
    # Asegurar una tarea a eliminar
    col_p = cli.proyecto_actual.listar_columnas()[0]
    tarea = col_p.tareas[0]
    feed_inputs(monkeypatch, ["9", "s"])  # Eliminar y confirmar
    cli.editar_tarea(col_p, tarea)
    out = capsys.readouterr().out
    assert "Eliminar tarea" in out
    assert "Tarea eliminada" in out
    assert tarea not in col_p.tareas


# HU-004 CA-11: Fecha de modificación automática tras cambiar
def test_hu004_ca11_fecha_modificacion_actualizada(cli, monkeypatch, capsys):
    col_p = cli.proyecto_actual.listar_columnas()[0]
    tarea = Tarea("Editar CA11", "Desc")
    col_p.agregar_tarea(tarea)
    prev_mod = tarea.fecha_modificacion
    feed_inputs(monkeypatch, ["2", "Cambio de prueba", "0"])  # Cambiar descripción y guardar
    cli.editar_tarea(col_p, tarea)
    out = capsys.readouterr().out
    assert "Cambios guardados" in out
    assert tarea.fecha_modificacion != prev_mod


# HU-004 CA-12: Guardado automático tras cada edición
def test_hu004_ca12_guardado_automatico(cli, monkeypatch):
    col_p = cli.proyecto_actual.listar_columnas()[0]
    tarea = Tarea("Editar CA12", "Desc")
    col_p.agregar_tarea(tarea)
    prev = len(cli.storage.saved_projects)
    feed_inputs(monkeypatch, ["3", "3", "0"])  # Cambiar prioridad a Alta y guardar
    cli.editar_tarea(col_p, tarea)
    assert len(cli.storage.saved_projects) == prev + 1