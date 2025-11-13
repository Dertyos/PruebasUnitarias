from models import Usuario


def feed(monkeypatch, inputs):
    it = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(it))


def crear_proyecto_y_tareas_para_stats(app, monkeypatch):
    app.usuario_actual = Usuario("Owner", "owner@s5.com")
    feed(monkeypatch, ["Proyecto Stats", "", ""])  
    app.crear_proyecto()
    app.proyecto_actual = app.storage.cargar_todos_proyectos()[0]
    feed(monkeypatch, ["Pendiente T", "", "2", "1", "", ""])  
    app.agregar_tarea()
    feed(monkeypatch, ["Progreso T", "", "3", "2", "", ""])  
    app.agregar_tarea()
    feed(monkeypatch, ["Completada T", "", "1", "3", "", ""])  
    app.agregar_tarea()
    feed(monkeypatch, ["Bloqueada T", "", "4", "1", "", ""])  
    app.agregar_tarea()
    feed(monkeypatch, ["Progreso T", "1", "4", "2", "0", ""])  
    app.buscar_tarea()


def test_HU008_CA1_mostrar_estadisticas_por_estado(app, monkeypatch, capsys):
    crear_proyecto_y_tareas_para_stats(app, monkeypatch)
    feed(monkeypatch, [""])
    app.ver_estadisticas()
    out = capsys.readouterr().out
    assert "POR ESTADO:" in out and "Pendiente:" in out and "En Progreso:" in out and "Completada:" in out and "Bloqueada:" in out


def test_HU008_CA2_mostrar_estadisticas_por_prioridad(app, monkeypatch, capsys):
    crear_proyecto_y_tareas_para_stats(app, monkeypatch)
    feed(monkeypatch, [""])
    app.ver_estadisticas()
    out = capsys.readouterr().out
    assert "POR PRIORIDAD:" in out and "Urgente:" in out and "Alta:" in out and "Media:" in out and "Baja:" in out


def test_HU008_CA6_asignacion_porcentajes(app, monkeypatch, capsys):
    crear_proyecto_y_tareas_para_stats(app, monkeypatch)
    feed(monkeypatch, ["Pendiente T", "1", "5", "UsuarioX", "0", ""])  
    app.buscar_tarea()
    feed(monkeypatch, [""])
    app.ver_estadisticas()
    out = capsys.readouterr().out
    assert "ASIGNACION:" in out and "%" in out


def test_HU008_CA8_conteo_tareas_por_columna(app, monkeypatch, capsys):
    crear_proyecto_y_tareas_para_stats(app, monkeypatch)
    feed(monkeypatch, [""])
    app.ver_estadisticas()
    out = capsys.readouterr().out
    assert "POR COLUMNA:" in out and ":" in out


def test_HU008_CA7_tablero_total_tareas_por_columna_desde_stats(app, monkeypatch, capsys):
    crear_proyecto_y_tareas_para_stats(app, monkeypatch)
    feed(monkeypatch, [""])
    app.ver_estadisticas()
    out = capsys.readouterr().out
    assert "Pendiente:" in out or "En Progreso:" in out or "Completada:" in out


def test_HU008_CA9_tareas_retrasadas_no_implementado(app, monkeypatch, capsys):
    crear_proyecto_y_tareas_para_stats(app, monkeypatch)
    feed(monkeypatch, [""])
    app.ver_estadisticas()
    out = capsys.readouterr().out
    assert "Retrasadas" not in out


def test_HU009_CA1_exportar_csv_no_disponible(app, monkeypatch, capsys):
    crear_proyecto_y_tareas_para_stats(app, monkeypatch)
    feed(monkeypatch, ["6"])  
    app.mostrar_menu_proyecto_actual()
    out = capsys.readouterr().out
    assert "exportar" not in out.lower()


def test_HU009_CA5_exportar_json_no_disponible(app, monkeypatch, capsys):
    crear_proyecto_y_tareas_para_stats(app, monkeypatch)
    feed(monkeypatch, ["6"])  
    app.mostrar_menu_proyecto_actual()
    out = capsys.readouterr().out
    assert "exportar" not in out.lower()


def test_HU009_CA6_nombres_archivos_descriptivos_no_disponible(app, monkeypatch, capsys):
    crear_proyecto_y_tareas_para_stats(app, monkeypatch)
    feed(monkeypatch, ["6"])  
    app.mostrar_menu_proyecto_actual()
    out = capsys.readouterr().out
    assert "exportar" not in out.lower()