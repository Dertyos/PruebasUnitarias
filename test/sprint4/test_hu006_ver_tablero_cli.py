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
    # Stub del StorageManager
    monkeypatch.setattr(cli_module, "StorageManager", DummyStorage)
    monkeypatch.setattr(cli_module.os, "system", lambda *args, **kwargs: 0)

    interfaz = cli_module.CliInterface()
    interfaz.proyecto_actual = Proyecto("Proyecto Tablero", propietario_id="owner-1")
    col_p = interfaz.proyecto_actual.agregar_columna("Pendiente")
    col_ep = interfaz.proyecto_actual.agregar_columna("En Progreso")
    col_c = interfaz.proyecto_actual.agregar_columna("Completada")
    # Sembrar tareas con distintas prioridades y asignaciones
    t_u = Tarea("Urgente T1", "", prioridad="Urgente", asignado_a="Ana")
    t_a = Tarea("Alta T2", "", prioridad="Alta")
    t_m = Tarea("Media T3", "", prioridad="Media", asignado_a="Luis")
    t_b = Tarea("Baja T4", "", prioridad="Baja")
    col_p.agregar_tarea(t_u)
    col_p.agregar_tarea(t_a)
    col_ep.agregar_tarea(t_m)
    col_ep.agregar_tarea(t_b)
    # col_c queda vacío para validar "(vacio)"
    return interfaz


def feed_inputs(monkeypatch, values):
    it = iter(values)
    def _mock_input(prompt=None):
        if prompt is not None:
            print(prompt, end="")
        return next(it)
    monkeypatch.setattr(builtins, "input", _mock_input)


# CA-1: Mostrar todas las columnas del proyecto actual
def test_hu006_ca1_mostrar_todas_columnas(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, [""])  # continuar
    cli.ver_tablero()
    out = capsys.readouterr().out
    assert "TABLERO: Proyecto Tablero" in out
    assert "+- Pendiente (2 tareas)" in out
    assert "+- En Progreso (2 tareas)" in out
    assert "+- Completada (0 tareas)" in out


# CA-2: Mostrar todas las tareas dentro de cada columna
def test_hu006_ca2_mostrar_todas_tareas_en_columnas(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, [""])  # continuar
    cli.ver_tablero()
    out = capsys.readouterr().out
    assert "Urgente T1" in out
    assert "Alta T2" in out
    assert "Media T3" in out
    assert "Baja T4" in out


# CA-3: Mostrar el título de cada tarea en el tablero
def test_hu006_ca3_mostrar_titulo_de_cada_tarea(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, [""])  # continuar
    cli.ver_tablero()
    out = capsys.readouterr().out
    assert "Urgente T1" in out
    assert "Alta T2" in out
    assert "Media T3" in out
    assert "Baja T4" in out


# CA-4/5: Mostrar ID abreviado y asignado o "Sin asignar"
def test_hu006_ca4_id_abreviado(cli, monkeypatch, capsys):
    col_p = cli.proyecto_actual.listar_columnas()[0]
    t_u = col_p.tareas[0]
    col_ep = cli.proyecto_actual.listar_columnas()[1]
    t_m = col_ep.tareas[0]

    feed_inputs(monkeypatch, [""])  # continuar
    cli.ver_tablero()
    out = capsys.readouterr().out
    # ID abreviado
    assert t_u.tarea_id[:8] in out
    assert t_m.tarea_id[:8] in out


# CA-5: Mostrar asignado o 'Sin asignar'
def test_hu006_ca5_asignacion(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, [""])  # continuar
    cli.ver_tablero()
    out = capsys.readouterr().out
    assert "Asignado: Ana" in out
    assert "Asignado: Sin asignar" in out


# CA-6: Iconos de prioridad (mapeo actual del CLI)
def test_hu006_ca6_iconos_prioridad_completos(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, [""])  # continuar
    cli.ver_tablero()
    out = capsys.readouterr().out
    # Verificar iconos según implementación actual
    assert "!! Urgente T1" in out  # Urgente -> !!
    assert "[A] Alta T2" in out    # Alta -> [A]
    assert "[M] Media T3" in out   # Media -> [M]
    assert "[B] Baja T4" in out    # Baja -> [B]


# CA-7: Mostrar el conteo total de tareas en cada columna
def test_hu006_ca7_conteo_total_por_columna(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, [""])  # continuar
    cli.ver_tablero()
    out = capsys.readouterr().out
    assert "+- Pendiente (2 tareas)" in out
    assert "+- En Progreso (2 tareas)" in out
    assert "+- Completada (0 tareas)" in out


# CA-8: Mostrar '(vacio)' en columnas sin tareas
def test_hu006_ca8_columnas_vacias_muestran_vacio(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, [""])  # continuar
    cli.ver_tablero()
    out = capsys.readouterr().out
    assert "(vacio)" in out


# CA-9: Layout legible y organizado
def test_hu006_ca9_layout_legible(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, [""])  # continuar
    cli.ver_tablero()
    out = capsys.readouterr().out
    # Separadores y estructura clara
    assert "----------------------------------------" in out  # 40 guiones
    assert "+---------------------------------------" in out  # cierre de columna ('+' + 39 guiones)


# CA-10: Volver al menú anterior desde la vista del tablero
def test_hu006_ca10_volver_menu(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, [""])  # presionar Enter
    cli.ver_tablero()
    out = capsys.readouterr().out
    assert "Presione Enter para continuar..." in out