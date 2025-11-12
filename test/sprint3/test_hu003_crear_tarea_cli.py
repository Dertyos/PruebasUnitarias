import builtins
import types
import pytest

# Pruebas de Sprint 3 - HU-003: Crear Tarea (CLI)
# Nos guiamos por sprint3Cases.json y Historias de usuario.md

from models import Proyecto
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
    # Evitar limpiar pantalla
    monkeypatch.setattr(cli_module.os, "system", lambda *args, **kwargs: 0)

    interfaz = cli_module.CliInterface()
    # Proyecto actual con columnas por defecto
    interfaz.proyecto_actual = Proyecto("Proyecto Sprint3", propietario_id="owner-1")
    interfaz.proyecto_actual.agregar_columna("Pendiente")
    interfaz.proyecto_actual.agregar_columna("En Progreso")
    interfaz.proyecto_actual.agregar_columna("Completada")
    return interfaz


def feed_inputs(monkeypatch, values):
    it = iter(values)
    monkeypatch.setattr(builtins, "input", lambda prompt=None: next(it))


# HU-003 CA-1: Crear tarea con título obligatorio
def test_hu003_ca1_crear_tarea_titulo_obligatorio(cli, monkeypatch, capsys):
    feed_inputs(
        monkeypatch,
        [
            "Tarea CA1",  # Titulo
            "Detalle inicial",  # Descripcion
            "2",  # Prioridad Media
            "1",  # Columna Pendiente
            "Julian",  # Asignado a
            "",  # Continuar
        ],
    )

    cli.agregar_tarea()
    out = capsys.readouterr().out
    assert "AGREGAR NUEVA TAREA" in out
    assert "Tarea 'Tarea CA1' agregada a 'Pendiente'" in out

    # Verificar que la tarea está en la columna correcta
    columna = cli.proyecto_actual.listar_columnas()[0]
    assert columna.nombre == "Pendiente"
    assert columna.contar_tareas() == 1
    tarea = columna.tareas[0]
    assert tarea.titulo == "Tarea CA1"
    assert tarea.descripcion == "Detalle inicial"
    assert tarea.prioridad == "Media"
    assert tarea.asignado_a == "Julian"
    # Guardado automático
    assert len(cli.storage.saved_projects) >= 1


# HU-003 CA-2: Validar título obligatorio no vacío
def test_hu003_ca2_titulo_obligatorio_no_vacio(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, ["", ""])  # Titulo vacío, continuar
    cli.agregar_tarea()
    out = capsys.readouterr().out
    assert "El titulo no puede estar vacio" in out


# HU-003 CA-3: Descripción opcional
def test_hu003_ca3_descripcion_opcional(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, ["Tarea CA3", "", "1", "1", "", ""])  # Enter en descripción
    cli.agregar_tarea()
    out = capsys.readouterr().out
    assert "AGREGAR NUEVA TAREA" in out
    assert "Tarea 'Tarea CA3' agregada a 'Pendiente'" in out


# HU-003 CA-4: Seleccionar prioridad Urgente y ver detalles
def test_hu003_ca4_prioridad_urgente_ver_detalles(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, ["Tarea CA4", "", "4", "1", "", ""])  # Urgente
    cli.agregar_tarea()

    columna = cli.proyecto_actual.listar_columnas()[0]
    tarea = columna.tareas[-1]

    # Ver detalles en edición
    feed_inputs(monkeypatch, ["8", "0"])  # Ver detalles y guardar
    cli.editar_tarea(columna, tarea)
    out = capsys.readouterr().out
    assert "EDITAR TAREA: Tarea CA4" in out
    assert "Prioridad: Urgente" in out
    assert "Cambios guardados" in out


# HU-003 CA-5: Prioridad por defecto 'Media' si no se especifica
def test_hu003_ca5_prioridad_por_defecto_media(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, ["Tarea CA5", "", "", "1", "", ""])  # Enter en prioridad
    cli.agregar_tarea()
    columna = cli.proyecto_actual.listar_columnas()[0]
    tarea = columna.tareas[-1]

    feed_inputs(monkeypatch, ["8", "0"])  # Ver detalles
    cli.editar_tarea(columna, tarea)
    out = capsys.readouterr().out
    assert "Prioridad: Media" in out


# HU-003 CA-6: Seleccionar columna destino
def test_hu003_ca6_seleccionar_columna_destino(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, ["Tarea CA6", "", "2", "2", "", ""])  # Columna 2: En Progreso
    cli.agregar_tarea()
    out = capsys.readouterr().out
    assert "Tarea 'Tarea CA6' agregada a 'En Progreso'" in out

    columna = cli.proyecto_actual.listar_columnas()[1]
    assert any(t.titulo == "Tarea CA6" for t in columna.tareas)


# HU-003 CA-7: Asignación opcional de usuario
def test_hu003_ca7_asignacion_opcional_usuario(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, ["Tarea CA7", "", "3", "1", "Jeferson", ""])  # Alta
    cli.agregar_tarea()
    columna = cli.proyecto_actual.listar_columnas()[0]
    tarea = columna.tareas[-1]

    feed_inputs(monkeypatch, ["8", "0"])  # Ver detalles
    cli.editar_tarea(columna, tarea)
    out = capsys.readouterr().out
    assert "Asignado a: Jeferson" in out


# HU-003 CA-8: ID único (UUID) por tarea
def test_hu003_ca8_id_unico_por_tarea(cli, monkeypatch):
    feed_inputs(monkeypatch, ["Tarea CA8-1", "", "2", "1", "", ""])  # Media
    cli.agregar_tarea()
    feed_inputs(monkeypatch, ["Tarea CA8-2", "", "2", "1", "", ""])  # Media
    cli.agregar_tarea()

    columna = cli.proyecto_actual.listar_columnas()[0]
    t1 = columna.tareas[-2]
    t2 = columna.tareas[-1]
    assert t1.tarea_id and t2.tarea_id and t1.tarea_id != t2.tarea_id


# HU-003 CA-9: Estado inicial 'Pendiente'
def test_hu003_ca9_estado_inicial_pendiente(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, ["Tarea CA9", "", "2", "1", "", ""])  # Media
    cli.agregar_tarea()
    columna = cli.proyecto_actual.listar_columnas()[0]
    tarea = columna.tareas[-1]

    feed_inputs(monkeypatch, ["8", "0"])  # Ver detalles
    cli.editar_tarea(columna, tarea)
    out = capsys.readouterr().out
    assert "Estado: Pendiente" in out


# HU-003 CA-10: Fechas de creación y modificación automáticas
def test_hu003_ca10_fechas_automaticas(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, ["Tarea CA10", "", "2", "1", "", ""])  # Media
    cli.agregar_tarea()
    columna = cli.proyecto_actual.listar_columnas()[0]
    tarea = columna.tareas[-1]

    feed_inputs(monkeypatch, ["8", "0"])  # Ver detalles
    cli.editar_tarea(columna, tarea)
    out = capsys.readouterr().out
    assert "Creada: " in out
    assert "Modificada: " in out


# HU-003 CA-11: Guardado automático tras crear tarea
def test_hu003_ca11_guardado_automatico_tras_crear(cli, monkeypatch):
    prev = len(cli.storage.saved_projects)
    feed_inputs(monkeypatch, ["Tarea CA11", "", "2", "1", "", ""])  # Media
    cli.agregar_tarea()
    assert len(cli.storage.saved_projects) == prev + 1


# HU-003 CA-12: Mensaje de confirmación al crear
def test_hu003_ca12_confirmacion_al_crear(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, ["Tarea CA12", "", "2", "1", "", ""])  # Media
    cli.agregar_tarea()
    out = capsys.readouterr().out
    assert "Tarea 'Tarea CA12' agregada a 'Pendiente'" in out