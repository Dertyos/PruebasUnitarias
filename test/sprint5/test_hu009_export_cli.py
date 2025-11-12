import builtins
import pytest

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
    # Stub del StorageManager y limpiar pantalla
    monkeypatch.setattr(cli_module, "StorageManager", DummyStorage)
    monkeypatch.setattr(cli_module.os, "system", lambda *args, **kwargs: 0)

    interfaz = cli_module.CliInterface()
    interfaz.proyecto_actual = Proyecto("Proyecto Datos", propietario_id="owner-1")

    # Columnas y tareas mínimas para mostrar el menú con conteo
    col_p = interfaz.proyecto_actual.agregar_columna("Pendiente")
    col_ep = interfaz.proyecto_actual.agregar_columna("En Progreso")
    col_c = interfaz.proyecto_actual.agregar_columna("Completada")
    col_p.agregar_tarea(Tarea("T1", prioridad="Media"))
    col_ep.agregar_tarea(Tarea("T2", prioridad="Alta"))

    return interfaz


def feed_inputs(monkeypatch, values):
    it = iter(values)
    def _mock_input(prompt=None):
        if prompt is not None:
            print(prompt, end="")
        return next(it)
    monkeypatch.setattr(builtins, "input", _mock_input)


def _show_project_menu(cli, monkeypatch, capsys):
    """Helper para mostrar una vez el menú de proyecto actual y salir con '6'"""
    feed_inputs(monkeypatch, ["6"])  # salir de inmediato
    cli.mostrar_menu_proyecto_actual()
    return capsys.readouterr().out


# HU-009 CA-1: Exportar tareas a formato CSV (Bloqueado)
def test_hu009_ca1_exportar_csv_bloqueado(cli, monkeypatch, capsys):
    out = _show_project_menu(cli, monkeypatch, capsys)
    assert "PROYECTO: Proyecto Datos" in out
    # No hay opción de exportar en el menú
    assert "Exportar" not in out
    assert "CSV" not in out


# HU-009 CA-2: CSV incluye campos requeridos (Bloqueado)
def test_hu009_ca2_csv_campos_requeridos_bloqueado(cli, monkeypatch, capsys):
    out = _show_project_menu(cli, monkeypatch, capsys)
    assert "CSV" not in out


# HU-009 CA-3: Exportar a Markdown (Bloqueado)
def test_hu009_ca3_exportar_markdown_bloqueado(cli, monkeypatch, capsys):
    out = _show_project_menu(cli, monkeypatch, capsys)
    assert "Markdown" not in out


# HU-009 CA-4: Markdown con estructura jerárquica (Bloqueado)
def test_hu009_ca4_markdown_jerarquico_bloqueado(cli, monkeypatch, capsys):
    out = _show_project_menu(cli, monkeypatch, capsys)
    assert "Markdown" not in out
    assert "Jerarqu" not in out  # jerárquico/jerarquia


# HU-009 CA-5: Exportar a JSON (Bloqueado)
def test_hu009_ca5_exportar_json_bloqueado(cli, monkeypatch, capsys):
    out = _show_project_menu(cli, monkeypatch, capsys)
    assert "JSON" not in out


# HU-009 CA-6: Nombres de archivos descriptivos (Bloqueado)
def test_hu009_ca6_nombres_archivo_descriptivos_bloqueado(cli, monkeypatch, capsys):
    out = _show_project_menu(cli, monkeypatch, capsys)
    assert "Exportar" not in out
    assert "archivo" not in out.lower()


# HU-009 CA-7: Codificación UTF-8 (Bloqueado)
def test_hu009_ca7_codificacion_utf8_bloqueado(cli, monkeypatch, capsys):
    out = _show_project_menu(cli, monkeypatch, capsys)
    assert "UTF-8" not in out


# HU-009 CA-8: Mensaje de confirmación tras exportar (Bloqueado)
def test_hu009_ca8_confirmacion_export_bloqueado(cli, monkeypatch, capsys):
    out = _show_project_menu(cli, monkeypatch, capsys)
    assert "exportar" not in out.lower()
    assert "confirm" not in out.lower()  # confirmación


# HU-009 CA-9: Datos completos, precisos y consistentes (Bloqueado)
def test_hu009_ca9_integridad_datos_bloqueado(cli, monkeypatch, capsys):
    out = _show_project_menu(cli, monkeypatch, capsys)
    assert "Exportar" not in out


# HU-009 CA-10: Eficiencia de exportación (Bloqueado)
def test_hu009_ca10_eficiencia_export_bloqueado(cli, monkeypatch, capsys):
    out = _show_project_menu(cli, monkeypatch, capsys)
    assert "Exportar" not in out