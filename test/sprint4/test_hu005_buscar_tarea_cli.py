import builtins
import time
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
    interfaz.proyecto_actual = Proyecto("Proyecto Sprint4", propietario_id="owner-1")
    col_p = interfaz.proyecto_actual.agregar_columna("Pendiente")
    col_ep = interfaz.proyecto_actual.agregar_columna("En Progreso")
    interfaz.proyecto_actual.agregar_columna("Completada")
    # Sembrar tareas
    t1 = Tarea("Tarea Buscar Uno", "Desc uno", prioridad="Alta", asignado_a="Ana")
    t2 = Tarea("Tarea buscar Dos", "Descripcion DOS", prioridad="Media")
    t3 = Tarea("Otra cosa", "Buscar en descripcion", prioridad="Baja")
    # Casos específicos de búsqueda parcial y case-insensitive
    t_impl = Tarea("Implementar funcionalidad", "Detalles de implementación", prioridad="Media")
    t_imp = Tarea("Tarea Importante", "", prioridad="Alta")
    t_doc = Tarea("Doc Tarea", "Revisar código y documentación", prioridad="Baja")
    col_p.agregar_tarea(t1)
    col_p.agregar_tarea(t2)
    col_p.agregar_tarea(t_impl)
    col_ep.agregar_tarea(t3)
    col_ep.agregar_tarea(t_imp)
    col_p.agregar_tarea(t_doc)
    return interfaz


def feed_inputs(monkeypatch, values):
    it = iter(values)
    def _mock_input(prompt=None):
        if prompt is not None:
            print(prompt, end="")
        return next(it)
    monkeypatch.setattr(builtins, "input", _mock_input)


# CA-1: Ingresar un término de búsqueda
def test_hu005_ca1_ingresar_termino_busqueda(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, ["buscar", "0", ""])  # término, cancelar, continuar
    cli.buscar_tarea()
    out = capsys.readouterr().out
    assert "Ingrese el titulo o parte de el para buscar:" in out
    assert "RESULTADOS DE BUSQUEDA" in out


# CA-2: Buscar en títulos de tareas (búsqueda parcial)
def test_hu005_ca2_busca_en_titulos_parcial(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, ["Implementar", "0", ""])  # término, cancelar, continuar
    cli.buscar_tarea()
    out = capsys.readouterr().out
    assert "Implementar funcionalidad" in out


# CA-3: Buscar en descripciones de tareas (búsqueda parcial)
def test_hu005_ca3_busca_en_descripciones_parcial(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, ["documentación", "0", ""])  # término, cancelar, continuar
    cli.buscar_tarea()
    out = capsys.readouterr().out
    assert "Doc Tarea" in out


# CA-4: Búsqueda insensible a mayúsculas y minúsculas
def test_hu005_ca4_insensible_mayusculas_minusculas(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, ["IMPORTANTE", "0", ""])  # término, cancelar, continuar
    cli.buscar_tarea()
    out = capsys.readouterr().out
    assert "Tarea Importante" in out


# CA-5: Mostrar número total de tareas encontradas
def test_hu005_ca5_muestra_numero_resultados(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, ["tarea buscar", "0", ""])  # término (coincide con dos), cancelar, continuar
    cli.buscar_tarea()
    out = capsys.readouterr().out
    assert "RESULTADOS DE BUSQUEDA: 2 tareas encontradas" in out


# CA-6: Mostrar columna de cada tarea encontrada
def test_hu005_ca6_muestra_columna_en_resultados(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, ["descripcion", "0", ""])  # coincide con t3 en En Progreso
    cli.buscar_tarea()
    out = capsys.readouterr().out
    assert "(en 'En Progreso')" in out


# CA-7: Seleccionar una tarea de resultados para editar
def test_hu005_ca7_seleccionar_tarea_para_editar(cli, monkeypatch, capsys):
    # Buscar y seleccionar la primera tarea, luego ver detalles y guardar
    feed_inputs(monkeypatch, ["buscar", "1", "8", "0", ""])  # término, seleccionar 1, ver detalles, guardar, continuar
    cli.buscar_tarea()
    out = capsys.readouterr().out
    assert "EDITAR TAREA:" in out
    assert "Cambios guardados" in out


# CA-8: Mensaje claro si no hay resultados
def test_hu005_ca8_sin_resultados_mensaje_claro(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, ["inexistente", ""])  # término que no coincide, continuar
    cli.buscar_tarea()
    out = capsys.readouterr().out
    assert "No se encontraron tareas" in out


# CA-9 (Divergencia actual): El término vacío no retorna todas, muestra error
def test_hu005_ca9_termino_vacio_muestra_error(cli, monkeypatch, capsys):
    feed_inputs(monkeypatch, ["", ""])  # término vacío, continuar
    cli.buscar_tarea()
    out = capsys.readouterr().out
    assert "El termino de busqueda no puede estar vacio" in out


# CA-10: Eficiencia de búsqueda con muchas tareas
def test_hu005_ca10_eficiencia_con_muchas_tareas(cli, monkeypatch, capsys):
    # Sembrar 60 tareas adicionales con término 'bulkterm' en títulos
    col0 = cli.proyecto_actual.listar_columnas()[0]
    for i in range(60):
        col0.agregar_tarea(Tarea(f"bulkterm-{i}", "", prioridad="Media"))

    start = time.perf_counter()
    feed_inputs(monkeypatch, ["bulkterm", "0", ""])  # buscar, cancelar, continuar
    cli.buscar_tarea()
    duration = time.perf_counter() - start
    out = capsys.readouterr().out
    assert "RESULTADOS DE BUSQUEDA" in out
    # Umbral razonable según casos: < 2s
    assert duration < 2.0