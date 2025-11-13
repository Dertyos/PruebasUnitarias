import uuid
from datetime import datetime

from models import Usuario
from storage import StorageManager


def feed(monkeypatch, inputs):
    it = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(it))


def crear_proyecto_actual(app, monkeypatch, nombre="Proyecto Sprint3"):
    app.usuario_actual = Usuario("Owner", "owner@s3.com")
    feed(monkeypatch, [nombre, "", ""])  
    app.crear_proyecto()
    app.proyecto_actual = app.storage.cargar_todos_proyectos()[0]


def test_HU003_CA1_crear_tarea_titulo_obligatorio(app, monkeypatch, capsys):
    crear_proyecto_actual(app, monkeypatch)
    feed(monkeypatch, ["Tarea CA1", "Detalle inicial", "2", "1", "Julian", ""])  
    app.agregar_tarea()
    out = capsys.readouterr().out
    assert "Tarea 'Tarea CA1' agregada a 'Pendiente'" in out


def test_HU003_CA2_titulo_no_vacio(app, monkeypatch, capsys):
    crear_proyecto_actual(app, monkeypatch)
    feed(monkeypatch, ["", ""])  
    app.agregar_tarea()
    out = capsys.readouterr().out
    assert "El titulo no puede estar vacio" in out


def test_HU003_CA3_descripcion_opcional(app, monkeypatch, capsys):
    crear_proyecto_actual(app, monkeypatch)
    feed(monkeypatch, ["Tarea CA3", "", "1", "1", "", ""])  
    app.agregar_tarea()
    out = capsys.readouterr().out
    assert "Tarea 'Tarea CA3'" in out


def test_HU003_CA4_prioridad_urgente_y_ver_detalles(app, monkeypatch, capsys):
    crear_proyecto_actual(app, monkeypatch)
    feed(monkeypatch, ["Tarea CA4", "", "4", "1", "", ""])  
    app.agregar_tarea()
    feed(monkeypatch, ["Tarea CA4", "1", "8", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "Prioridad: Urgente" in out


def test_HU003_CA5_prioridad_por_defecto_media(app, monkeypatch, capsys):
    crear_proyecto_actual(app, monkeypatch)
    feed(monkeypatch, ["Tarea CA5", "", "", "1", "", ""])  
    app.agregar_tarea()
    feed(monkeypatch, ["Tarea CA5", "1", "8", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "Prioridad: Media" in out


def test_HU003_CA6_seleccionar_columna_destino_en_progreso(app, monkeypatch, capsys):
    crear_proyecto_actual(app, monkeypatch)
    feed(monkeypatch, ["Tarea CA6", "", "2", "2", "", ""])  
    app.agregar_tarea()
    out = capsys.readouterr().out
    assert "agregada a 'En Progreso'" in out


def test_HU003_CA7_asignacion_opcional_usuario(app, monkeypatch, capsys):
    crear_proyecto_actual(app, monkeypatch)
    feed(monkeypatch, ["Tarea CA7", "", "3", "1", "Jeferson", ""])  
    app.agregar_tarea()
    feed(monkeypatch, ["Tarea CA7", "1", "8", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "Asignado a: Jeferson" in out


def test_HU003_CA8_uuid_en_tarea(app, monkeypatch, capsys):
    crear_proyecto_actual(app, monkeypatch)
    feed(monkeypatch, ["Tarea CA8", "", "2", "1", "", ""])  
    app.agregar_tarea()
    feed(monkeypatch, ["Tarea CA8", "1", "8", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "ID:" in out
    datos = app.storage.cargar_datos()["proyectos"][0]
    tarea = [t for c in datos["columnas"] for t in c["tareas"] if t["titulo"] == "Tarea CA8"][0]
    assert isinstance(uuid.UUID(tarea["tarea_id"]), uuid.UUID)


def test_HU003_CA9_estado_inicial_pendiente(app, monkeypatch, capsys):
    crear_proyecto_actual(app, monkeypatch)
    feed(monkeypatch, ["Tarea CA9", "", "2", "1", "", ""])  
    app.agregar_tarea()
    feed(monkeypatch, ["Tarea CA9", "1", "8", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "Estado: Pendiente" in out


def test_HU003_CA10_fechas_creacion_y_modificacion(app, monkeypatch):
    crear_proyecto_actual(app, monkeypatch)
    feed(monkeypatch, ["Tarea CA10", "", "2", "1", "", ""])  
    app.agregar_tarea()
    datos = app.storage.cargar_datos()["proyectos"][0]
    tarea = [t for c in datos["columnas"] for t in c["tareas"] if t["titulo"] == "Tarea CA10"][0]
    assert datetime.fromisoformat(tarea["fecha_creacion"]) and datetime.fromisoformat(tarea["fecha_modificacion"])


def test_HU003_CA11_guardado_automatico_tras_crear_tarea(app, monkeypatch):
    crear_proyecto_actual(app, monkeypatch)
    feed(monkeypatch, ["Tarea CA11", "", "2", "1", "", ""])  
    app.agregar_tarea()
    nuevo = StorageManager(app.storage.archivo_datos)
    proyecto = nuevo.cargar_todos_proyectos()[0]
    assert any(t.titulo == "Tarea CA11" for t in proyecto.obtener_todas_las_tareas())


def test_HU003_CA12_mensaje_confirmacion_al_crear(app, monkeypatch, capsys):
    crear_proyecto_actual(app, monkeypatch)
    feed(monkeypatch, ["Tarea CA12", "", "2", "1", "", ""])  
    app.agregar_tarea()
    out = capsys.readouterr().out
    assert "Tarea 'Tarea CA12' agregada" in out


def preparar_tarea_para_edicion(app, monkeypatch, titulo="Editar CA1"):
    crear_proyecto_actual(app, monkeypatch)
    feed(monkeypatch, [titulo, "", "2", "1", "", ""])  
    app.agregar_tarea()


def test_HU004_CA1_cambiar_titulo(app, monkeypatch, capsys):
    preparar_tarea_para_edicion(app, monkeypatch, "Editar CA1")
    feed(monkeypatch, ["Editar CA1", "1", "1", "Editar CA1 Renombrada", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "Cambios guardados" in out


def test_HU004_CA2_cambiar_descripcion(app, monkeypatch, capsys):
    preparar_tarea_para_edicion(app, monkeypatch, "Editar CA2")
    feed(monkeypatch, ["Editar CA2", "1", "2", "Descripción actualizada", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "Cambios guardados" in out


def test_HU004_CA3_cambiar_prioridad_a_urgente(app, monkeypatch, capsys):
    preparar_tarea_para_edicion(app, monkeypatch, "Editar CA3")
    feed(monkeypatch, ["Editar CA3", "1", "3", "4", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "Cambios guardados" in out


def test_HU004_CA4_cambiar_estado_en_progreso(app, monkeypatch, capsys):
    preparar_tarea_para_edicion(app, monkeypatch, "Editar CA4")
    feed(monkeypatch, ["Editar CA4", "1", "4", "2", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "Cambios guardados" in out


def test_HU004_CA5_cambiar_asignado(app, monkeypatch, capsys):
    preparar_tarea_para_edicion(app, monkeypatch, "Editar CA5")
    feed(monkeypatch, ["Editar CA5", "1", "5", "Jeferson", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "Cambios guardados" in out


def test_HU004_CA6_mover_tarea_a_completada(app, monkeypatch, capsys):
    preparar_tarea_para_edicion(app, monkeypatch, "Editar CA6")
    feed(monkeypatch, ["Editar CA6", "1", "6", "3", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "Tarea movida" in out and "Cambios guardados" in out


def test_HU004_CA7_agregar_etiqueta(app, monkeypatch, capsys):
    preparar_tarea_para_edicion(app, monkeypatch, "Editar CA7")
    feed(monkeypatch, ["Editar CA7", "1", "7", "backend", "8", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "Etiqueta agregada" in out and "Etiquetas:" in out


def test_HU004_CA8_eliminar_etiqueta_no_disponible(app, monkeypatch, capsys):
    preparar_tarea_para_edicion(app, monkeypatch, "Editar CA8")
    feed(monkeypatch, ["Editar CA8", "1", "7", "backend", "8", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "Eliminar etiqueta" not in out


def test_HU004_CA9_ver_detalles_completos(app, monkeypatch, capsys):
    preparar_tarea_para_edicion(app, monkeypatch, "Editar CA9")
    feed(monkeypatch, ["Editar CA9", "1", "8", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "ID:" in out and "Titulo:" in out and "Descripcion:" in out and "Prioridad:" in out and "Estado:" in out and "Asignado a:" in out and "Etiquetas:" in out


def test_HU004_CA10_eliminar_tarea_con_confirmacion(app, monkeypatch, capsys):
    preparar_tarea_para_edicion(app, monkeypatch, "Editar CA10")
    feed(monkeypatch, ["Editar CA10", "1", "9", "s", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "Tarea eliminada" in out


def test_HU004_CA11_fecha_modificacion_tras_cambiar(app, monkeypatch):
    preparar_tarea_para_edicion(app, monkeypatch, "Editar CA11")
    feed(monkeypatch, ["Editar CA11", "1", "2", "Cambio de prueba", "0", ""])  
    app.buscar_tarea()
    datos = app.storage.cargar_datos()["proyectos"][0]
    tarea = [t for c in datos["columnas"] for t in c["tareas"] if t["titulo"] == "Editar CA11"][0]
    assert datetime.fromisoformat(tarea["fecha_modificacion"]) >= datetime.fromisoformat(tarea["fecha_creacion"])


def test_HU004_CA12_guardado_automatico_tras_edicion(app, monkeypatch, capsys):
    preparar_tarea_para_edicion(app, monkeypatch, "Editar CA12")
    feed(monkeypatch, ["Editar CA12", "1", "3", "3", "0", ""])  
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "Cambios guardados" in out