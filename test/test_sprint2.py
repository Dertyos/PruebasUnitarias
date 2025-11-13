import uuid
from datetime import datetime

import pytest

from models import Usuario
from storage import StorageManager


def feed(monkeypatch, inputs):
    it = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(it))


# HU-002: Proyectos

def test_HU002_CA1_crear_proyecto_con_nombre_y_descripcion(app, monkeypatch, capsys):
    app.usuario_actual = Usuario("Owner", "owner@test.com")
    feed(monkeypatch, ["Proyecto Test", "Descripción de prueba", ""])  
    app.crear_proyecto()
    out = capsys.readouterr().out
    assert "Proyecto 'Proyecto Test' creado exitosamente" in out
    datos = app.storage.cargar_datos()["proyectos"][0]
    assert datos["descripcion"] == "Descripción de prueba"


def test_HU002_CA2_nombre_proyecto_obligatorio(app, monkeypatch, capsys):
    app.usuario_actual = Usuario("Owner", "owner@test.com")
    feed(monkeypatch, ["", ""])  
    app.crear_proyecto()
    out = capsys.readouterr().out
    assert "El nombre no puede estar vacio" in out
    assert app.storage.cargar_datos()["proyectos"] == []


def test_HU002_CA3_uuid_asignado_al_proyecto(app, monkeypatch):
    app.usuario_actual = Usuario("Owner", "owner@test.com")
    feed(monkeypatch, ["Proyecto UUID Test", "", ""])  
    app.crear_proyecto()
    datos = app.storage.cargar_datos()["proyectos"][0]
    assert isinstance(uuid.UUID(datos["proyecto_id"]), uuid.UUID)


def test_HU002_CA4_propietario_asignado_automaticamente(app, monkeypatch):
    owner = Usuario("Owner", "owner@test.com")
    app.usuario_actual = owner
    feed(monkeypatch, ["Proyecto Propietario", "", ""])  
    app.crear_proyecto()
    datos = app.storage.cargar_datos()["proyectos"][0]
    assert datos["propietario_id"] == owner.usuario_id


def test_HU002_CA5_columnas_por_defecto(app, monkeypatch):
    app.usuario_actual = Usuario("Owner", "owner@test.com")
    feed(monkeypatch, ["Proyecto Columnas", "", ""])  
    app.crear_proyecto()
    datos = app.storage.cargar_datos()["proyectos"][0]
    nombres = [c["nombre"] for c in datos["columnas"]]
    assert nombres == ["Pendiente", "En Progreso", "Completada"]


def test_HU002_CA6_abrir_proyecto_existente(app, monkeypatch, capsys):
    app.usuario_actual = Usuario("Owner", "owner@test.com")
    feed(monkeypatch, ["Proyecto Open", "", ""])  
    app.crear_proyecto()
    feed(monkeypatch, ["1", ""])  
    app.abrir_proyecto()
    out = capsys.readouterr().out
    assert "Proyecto actual: Proyecto Open" in out
    assert app.proyecto_actual is not None


def test_HU002_CA7_listar_proyectos_con_conteo(app, monkeypatch, capsys):
    app.usuario_actual = Usuario("Owner", "owner@test.com")
    feed(monkeypatch, ["Proyecto List", "", ""])  
    app.crear_proyecto()
    feed(monkeypatch, [""])  
    app.listar_proyectos()
    out = capsys.readouterr().out
    assert "PROYECTOS DISPONIBLES" in out
    assert "Proyecto List" in out
    assert "tareas" in out and "columnas" in out


def test_HU002_CA8_eliminar_proyecto_con_confirmacion(app, monkeypatch, capsys):
    app.usuario_actual = Usuario("Owner", "owner@test.com")
    feed(monkeypatch, ["Proyecto Delete", "", ""])  
    app.crear_proyecto()
    feed(monkeypatch, ["1", "s", ""])  
    app.eliminar_proyecto()
    out = capsys.readouterr().out
    assert "Proyecto eliminado" in out
    assert app.storage.cargar_datos()["proyectos"] == []


def test_HU002_CA9_guardado_fechas_creacion_y_modificacion(app, monkeypatch):
    app.usuario_actual = Usuario("Owner", "owner@test.com")
    feed(monkeypatch, ["Proyecto Fechas", "", ""])  
    app.crear_proyecto()
    datos = app.storage.cargar_datos()["proyectos"][0]
    assert datetime.fromisoformat(datos["fecha_creacion"]) 
    assert datetime.fromisoformat(datos["fecha_modificacion"]) 


def test_HU002_CA10_persistencia_automatica_en_json(app, monkeypatch):
    app.usuario_actual = Usuario("Owner", "owner@test.com")
    feed(monkeypatch, ["Proyecto Persistencia", "", ""])  
    app.crear_proyecto()
    nuevo = StorageManager(app.storage.archivo_datos)
    assert any(p.nombre == "Proyecto Persistencia" for p in nuevo.cargar_todos_proyectos())


# HU-007: Columnas

def crear_proyecto_actual(app, nombre="Proyecto Base", monkeypatch=None):
    app.usuario_actual = Usuario("Owner", "owner@test.com")
    if monkeypatch:
        feed(monkeypatch, [nombre, "", ""])  
    app.crear_proyecto()
    app.proyecto_actual = app.storage.cargar_todos_proyectos()[0]


def test_HU007_CA1_agregar_columna(app, monkeypatch, capsys):
    crear_proyecto_actual(app, monkeypatch=monkeypatch)
    feed(monkeypatch, ["a", "Revisión", "", "v"])  
    app.gestionar_columnas()
    out = capsys.readouterr().out
    assert "Columna agregada" in out
    datos = app.storage.cargar_datos()["proyectos"][0]
    assert any(c["nombre"] == "Revisión" for c in datos["columnas"])


def test_HU007_CA2_ver_lista_completa_columnas(app, monkeypatch, capsys):
    crear_proyecto_actual(app, monkeypatch=monkeypatch)
    feed(monkeypatch, ["v"])  
    app.gestionar_columnas()
    out = capsys.readouterr().out
    assert "Pendiente" in out and "En Progreso" in out and "Completada" in out


def test_HU007_CA3_renombrar_columna(app, monkeypatch, capsys):
    crear_proyecto_actual(app, monkeypatch=monkeypatch)
    feed(monkeypatch, ["r", "1", "Pendientes", "", "v"])  
    app.gestionar_columnas()
    out = capsys.readouterr().out
    assert "Columna renombrada" in out
    datos = app.storage.cargar_datos()["proyectos"][0]
    nombres = [c["nombre"] for c in datos["columnas"]]
    assert nombres[0] == "Pendientes"


def test_HU007_CA4_eliminar_columna_con_confirmacion(app, monkeypatch, capsys):
    crear_proyecto_actual(app, monkeypatch=monkeypatch)
    feed(monkeypatch, ["d", "1", "s", "", "v"])  
    app.gestionar_columnas()
    out = capsys.readouterr().out
    assert "Columna eliminada" in out
    datos = app.storage.cargar_datos()["proyectos"][0]
    assert len(datos["columnas"]) == 2


def test_HU007_CA5_eliminacion_tareas_al_eliminar_columna(app, monkeypatch, capsys):
    crear_proyecto_actual(app, monkeypatch=monkeypatch)
    feed(monkeypatch, ["Tarea Columna", "Desc", "2", "1", "", ""])  
    app.agregar_tarea()
    feed(monkeypatch, ["d", "1", "s", "", "v"])  
    app.gestionar_columnas()
    out = capsys.readouterr().out
    assert "Columna eliminada" in out
    proyecto = StorageManager(app.storage.archivo_datos).cargar_todos_proyectos()[0]
    assert all(t.titulo != "Tarea Columna" for t in proyecto.obtener_todas_las_tareas())


def test_HU007_CA6_conteo_tareas_por_columna(app, monkeypatch, capsys):
    crear_proyecto_actual(app, monkeypatch=monkeypatch)
    feed(monkeypatch, ["Tarea 1", "", "2", "1", "", ""])  
    app.agregar_tarea()
    feed(monkeypatch, ["v"])  
    app.gestionar_columnas()
    out = capsys.readouterr().out
    assert "Pendiente (1 tareas)" in out


def test_HU007_CA7_orden_de_columnas(app, monkeypatch):
    crear_proyecto_actual(app, monkeypatch=monkeypatch)
    feed(monkeypatch, ["a", "A", "", "a", "B", "", "v"])  
    app.gestionar_columnas()
    proyecto = StorageManager(app.storage.archivo_datos).cargar_todos_proyectos()[0]
    nombres = [c.nombre for c in proyecto.listar_columnas()]
    assert nombres == ["Pendiente", "En Progreso", "Completada", "A", "B"]


def test_HU007_CA8_nombre_columna_obligatorio(app, monkeypatch, capsys):
    crear_proyecto_actual(app, monkeypatch=monkeypatch)
    feed(monkeypatch, ["a", "", "v"])  
    app.gestionar_columnas()
    out = capsys.readouterr().out
    datos = app.storage.cargar_datos()["proyectos"][0]
    assert len(datos["columnas"]) == 3


def test_HU007_CA9_evitar_columnas_duplicadas(app, monkeypatch):
    crear_proyecto_actual(app, monkeypatch=monkeypatch)
    feed(monkeypatch, ["a", "Pendiente", "", "v"])  
    app.gestionar_columnas()
    datos = app.storage.cargar_datos()["proyectos"][0]
    nombres = [c["nombre"] for c in datos["columnas"]]
    assert nombres.count("Pendiente") <= 1


def test_HU007_CA10_guardado_automatico_cambios_columnas(app, monkeypatch):
    crear_proyecto_actual(app, monkeypatch=monkeypatch)
    feed(monkeypatch, ["a", "Nueva Columna", "", "v"])  
    app.gestionar_columnas()
    nuevo = StorageManager(app.storage.archivo_datos)
    proyecto = nuevo.cargar_todos_proyectos()[0]
    assert any(c.nombre == "Nueva Columna" for c in proyecto.columnas)