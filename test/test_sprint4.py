import time

from models import Usuario
from storage import StorageManager


def feed(monkeypatch, inputs):
    it = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(it))


def crear_proyecto_con_tareas(app, monkeypatch, nombre="Proyecto Sprint4"):
    app.usuario_actual = Usuario("Owner", "owner@s4.com")
    feed(monkeypatch, [nombre, "", ""])  
    app.crear_proyecto()
    app.proyecto_actual = app.storage.cargar_todos_proyectos()[0]
    feed(monkeypatch, ["Implementar funcionalidad", "desc", "2", "1", "", ""])  
    app.agregar_tarea()
    feed(monkeypatch, ["Revisar código y documentación", "doc y mas", "2", "2", "", ""])  
    app.agregar_tarea()
    feed(monkeypatch, ["Tarea Importante", "desc", "3", "3", "", ""])  
    app.agregar_tarea()


# HU-005 Búsqueda

def test_HU005_CA1_ingresar_termino_busqueda(app, monkeypatch, capsys):
    crear_proyecto_con_tareas(app, monkeypatch)
    feed(monkeypatch, ["test", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "RESULTADOS DE BUSQUEDA" in out or "No se encontraron tareas" in out


def test_HU005_CA2_busqueda_parcial_en_titulo(app, monkeypatch, capsys):
    crear_proyecto_con_tareas(app, monkeypatch)
    feed(monkeypatch, ["Implementar", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "Implementar funcionalidad" in out


def test_HU005_CA3_busqueda_parcial_en_descripcion(app, monkeypatch, capsys):
    crear_proyecto_con_tareas(app, monkeypatch)
    feed(monkeypatch, ["documentación", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "Revisar código y documentación" in out


def test_HU005_CA4_busqueda_insensible_mayus_minus(app, monkeypatch, capsys):
    crear_proyecto_con_tareas(app, monkeypatch)
    feed(monkeypatch, ["IMPORTANTE", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "Tarea Importante" in out


def test_HU005_CA5_mostrar_numero_total_encontradas(app, monkeypatch, capsys):
    crear_proyecto_con_tareas(app, monkeypatch)
    feed(monkeypatch, ["a", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "RESULTADOS DE BUSQUEDA:" in out


def test_HU005_CA6_mostrar_columna_de_cada_resultado(app, monkeypatch, capsys):
    crear_proyecto_con_tareas(app, monkeypatch)
    feed(monkeypatch, ["Revisar", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "(en 'En Progreso')" in out


def test_HU005_CA7_seleccionar_tarea_para_editar(app, monkeypatch, capsys):
    crear_proyecto_con_tareas(app, monkeypatch)
    feed(monkeypatch, ["Implementar", "1", "8", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "EDITAR TAREA: Implementar funcionalidad" in out


def test_HU005_CA8_termino_busqueda_vacio(app, monkeypatch, capsys):
    crear_proyecto_con_tareas(app, monkeypatch)
    feed(monkeypatch, ["", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "El termino de busqueda no puede estar vacio" in out


def test_HU005_CA10_eficiencia_con_muchas_tareas(app, monkeypatch, capsys):
    app.usuario_actual = Usuario("Owner", "owner@s4.com")
    feed(monkeypatch, ["Perf", "", ""])  
    app.crear_proyecto()
    app.proyecto_actual = app.storage.cargar_todos_proyectos()[0]
    for i in range(60):
        feed(monkeypatch, [f"Perf {i}", "", "2", "1", "", ""])  
        app.agregar_tarea()
    inicio = time.time()
    feed(monkeypatch, ["Perf", "0", ""])  
    app.buscar_tarea()
    dur = time.time() - inicio
    assert dur < 2.0


# HU-006 Tablero

def test_HU006_CA1_mostrar_todas_columnas(app, monkeypatch, capsys):
    crear_proyecto_con_tareas(app, monkeypatch)
    feed(monkeypatch, [""])  
    app.ver_tablero()
    out = capsys.readouterr().out
    assert "Pendiente" in out and "En Progreso" in out and "Completada" in out


def test_HU006_CA2_mostrar_tareas_por_columna(app, monkeypatch, capsys):
    crear_proyecto_con_tareas(app, monkeypatch)
    feed(monkeypatch, [""])  
    app.ver_tablero()
    out = capsys.readouterr().out
    assert "|" in out and "Implementar funcionalidad" in out


def test_HU006_CA4_iconos_de_prioridad(app, monkeypatch, capsys):
    app.usuario_actual = Usuario("Owner", "owner@s4.com")
    feed(monkeypatch, ["Proyecto Icons", "", ""])  
    app.crear_proyecto()
    app.proyecto_actual = app.storage.cargar_todos_proyectos()[0]
    feed(monkeypatch, ["Urgente T", "", "4", "1", "", ""])  
    app.agregar_tarea()
    feed(monkeypatch, ["Alta T", "", "3", "1", "", ""])  
    app.agregar_tarea()
    feed(monkeypatch, ["Media T", "", "2", "1", "", ""])  
    app.agregar_tarea()
    feed(monkeypatch, ["Baja T", "", "1", "1", "", ""])  
    app.agregar_tarea()
    feed(monkeypatch, [""])  
    app.ver_tablero()
    out = capsys.readouterr().out
    assert "!!" in out and "[A]" in out and "[M]" in out and "[B]" in out


def test_HU006_CA7_conteo_total_tareas_por_columna(app, monkeypatch, capsys):
    crear_proyecto_con_tareas(app, monkeypatch)
    feed(monkeypatch, [""])  
    app.ver_tablero()
    out = capsys.readouterr().out
    assert "(1 tareas)" in out or "(0 tareas)" in out


def test_HU006_CA8_vacio_en_columnas_sin_tareas(app, monkeypatch, capsys):
    app.usuario_actual = Usuario("Owner", "owner@s4.com")
    feed(monkeypatch, ["Proyecto Vacio", "", ""])  
    app.crear_proyecto()
    app.proyecto_actual = app.storage.cargar_todos_proyectos()[0]
    feed(monkeypatch, [""])  
    app.ver_tablero()
    out = capsys.readouterr().out
    assert "(vacio)" in out


def test_HU006_CA9_layout_legible(app, monkeypatch, capsys):
    crear_proyecto_con_tareas(app, monkeypatch)
    feed(monkeypatch, [""])  
    app.ver_tablero()
    out = capsys.readouterr().out
    assert "+" in out and "-" in out