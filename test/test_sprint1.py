import json
import shutil
import uuid
from datetime import datetime

import pytest

from storage import StorageManager
from models import Usuario


def feed(monkeypatch, inputs):
    it = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(it))


def test_HU001_CA1_crear_usuario_valido(app, monkeypatch, capsys):
    feed(monkeypatch, ["Usuario Valido", "valido@dominio.com", ""]) 
    app.crear_usuario()
    out = capsys.readouterr().out
    assert "Usuario 'Usuario Valido' creado exitosamente" in out
    datos = app.storage.cargar_datos()
    assert len(datos["usuarios"]) == 1
    assert datos["usuarios"][0]["email"] == "valido@dominio.com"


def test_HU001_CA2_email_invalido_rechazado(app, monkeypatch, capsys):
    feed(monkeypatch, ["Usuario Falla", "emailinvalido.com", ""]) 
    app.crear_usuario()
    out = capsys.readouterr().out
    assert "Email invalido" in out
    datos = app.storage.cargar_datos()
    assert datos["usuarios"] == []


def test_HU001_CA3_listar_usuarios_registrados(app, monkeypatch, capsys):
    feed(monkeypatch, ["Usuario Valido", "valido@dominio.com", ""]) 
    app.crear_usuario()
    feed(monkeypatch, [""]) 
    app.listar_usuarios()
    out = capsys.readouterr().out
    assert "USUARIOS REGISTRADOS" in out
    assert "Usuario Valido" in out


def test_HU001_CA4_marcar_usuario_actual_en_listado(app, monkeypatch, capsys):
    feed(monkeypatch, ["Usuario Uno", "uno@dominio.com", ""]) 
    app.crear_usuario()
    usuario = app.storage.cargar_todos_usuarios()[0]
    app.usuario_actual = usuario
    feed(monkeypatch, [""]) 
    app.listar_usuarios()
    out = capsys.readouterr().out
    assert " *" in out


def test_HU001_CA5_seleccionar_usuario_como_actual(app, monkeypatch, capsys):
    app.storage.guardar_usuario(Usuario("Usuario A", "a@dom.com"))
    app.storage.guardar_usuario(Usuario("Usuario B", "b@dom.com"))
    feed(monkeypatch, ["1", ""]) 
    app.seleccionar_usuario()
    out = capsys.readouterr().out
    assert "Usuario actual:" in out
    assert app.usuario_actual is not None


def test_HU001_CA6_eliminar_usuario_con_confirmacion(app, monkeypatch, capsys):
    app.storage.guardar_usuario(Usuario("Usuario Z", "z@dom.com"))
    feed(monkeypatch, ["1", "s", ""]) 
    app.eliminar_usuario()
    out = capsys.readouterr().out
    assert "Usuario eliminado" in out
    datos = app.storage.cargar_datos()
    assert datos["usuarios"] == []


def test_HU001_CA7_evitar_usuarios_duplicados_por_email(app, monkeypatch):
    feed(monkeypatch, ["User D1", "duplicado@dominio.com", ""]) 
    app.crear_usuario()
    feed(monkeypatch, ["User D2", "duplicado@dominio.com", ""]) 
    app.crear_usuario()
    datos = app.storage.cargar_datos()
    emails = [u["email"] for u in datos["usuarios"]]
    assert emails.count("duplicado@dominio.com") == 0


def test_HU001_CA8_uuid_asignado_a_cada_usuario(app, monkeypatch):
    feed(monkeypatch, ["Usuario UUID", "uuid@dom.com", ""]) 
    app.crear_usuario()
    datos = app.storage.cargar_datos()
    uid = datos["usuarios"][0]["usuario_id"]
    assert isinstance(uuid.UUID(uid), uuid.UUID)


def test_HU001_CA9_fecha_de_creacion_guardada(app, monkeypatch):
    feed(monkeypatch, ["Usuario Fecha", "fecha@dom.com", ""]) 
    app.crear_usuario()
    datos = app.storage.cargar_datos()
    ts = datos["usuarios"][0]["fecha_creacion"]
    assert datetime.fromisoformat(ts)


def test_HU001_CA10_persistencia_automatica_en_json(app, monkeypatch):
    feed(monkeypatch, ["Usuario Persist", "p@dom.com", ""]) 
    app.crear_usuario()
    sm = StorageManager(app.storage.archivo_datos)
    usuarios = sm.cargar_todos_usuarios()
    assert len(usuarios) == 1


def test_HU010_CA1_guardado_automatico_despues_de_crear_usuarios(app, monkeypatch):
    feed(monkeypatch, ["Auto User", "auto@dom.com", ""]) 
    app.crear_usuario()
    assert app.storage.archivo_datos.exists()


def test_HU010_CA2_guardado_automatico_despues_de_crear_proyectos(app, monkeypatch, capsys):
    app.usuario_actual = Usuario("Owner", "owner@dom.com")
    feed(monkeypatch, ["Proyecto Auto", "CA-2", ""]) 
    app.crear_proyecto()
    out = capsys.readouterr().out
    assert "Proyecto 'Proyecto Auto' creado exitosamente" in out
    proyectos = app.storage.cargar_todos_proyectos()
    assert len(proyectos) == 1


def test_HU010_CA3_guardado_automatico_despues_de_crear_tareas(app, monkeypatch, capsys):
    app.usuario_actual = Usuario("Owner", "owner@dom.com")
    feed(monkeypatch, ["Proyecto T", "", ""]) 
    app.crear_proyecto()
    app.proyecto_actual = app.storage.cargar_todos_proyectos()[0]
    feed(monkeypatch, ["Tarea CA-3", "Prueba", "2", "1", "", ""]) 
    app.agregar_tarea()
    out = capsys.readouterr().out
    assert "Tarea 'Tarea CA-3'" in out
    datos = app.storage.cargar_datos()["proyectos"][0]
    cols = datos["columnas"]
    pendientes = [c for c in cols if c["nombre"] == "Pendiente"][0]
    assert any(t["titulo"] == "Tarea CA-3" for t in pendientes["tareas"])


def test_HU010_CA4_guardado_automatico_despues_de_editar_tareas(app, monkeypatch, capsys):
    app.usuario_actual = Usuario("Owner", "owner@dom.com")
    feed(monkeypatch, ["Proyecto E", "", ""]) 
    app.crear_proyecto()
    app.proyecto_actual = app.storage.cargar_todos_proyectos()[0]
    feed(monkeypatch, ["Tarea CA-4", "", "2", "1", "", ""]) 
    app.agregar_tarea()
    feed(monkeypatch, ["Tarea CA-4", "1", "3", "3", "4", "2", "0", ""]) 
    app.buscar_tarea()
    out = capsys.readouterr().out
    assert "Cambios guardados" in out
    datos = app.storage.cargar_datos()["proyectos"][0]
    tarea = [t for c in datos["columnas"] for t in c["tareas"] if t["titulo"] == "Tarea CA-4"][0]
    assert tarea["prioridad"] == "Alta"
    assert tarea["estado"] == "En Progreso"


def test_HU010_CA5_guardado_automatico_despues_de_eliminar_datos(app, monkeypatch, capsys):
    app.storage.guardar_usuario(Usuario("User W", "w@dom.com"))
    feed(monkeypatch, ["1", "s", ""]) 
    app.eliminar_usuario()
    out = capsys.readouterr().out
    assert "Usuario eliminado" in out
    assert app.storage.cargar_datos()["usuarios"] == []


def test_HU010_CA6_datos_en_formato_json_bien_estructurado(app, monkeypatch):
    feed(monkeypatch, ["Usuario Json", "j@dom.com", ""]) 
    app.crear_usuario()
    feed(monkeypatch, ["Proyecto Json", "", ""]) 
    app.crear_proyecto()
    datos = app.storage.cargar_datos()
    assert set(datos.keys()) == {"proyectos", "usuarios"}


def test_HU010_CA7_creacion_automatica_carpeta_data(tmp_path):
    ruta = tmp_path / "custom" / "sub" / "projects.json"
    sm = StorageManager(ruta)
    assert ruta.parent.exists()


def test_HU010_CA8_creacion_automatica_projects_json(app, monkeypatch):
    feed(monkeypatch, ["Auto Proj", "", ""]) 
    app.crear_proyecto()
    assert app.storage.archivo_datos.exists()


def test_HU010_CA9_validacion_estructura_json_antes_de_guardar(app):
    datos = {"proyectos": [{"invalid": True}], "usuarios": []}
    ok = app.storage.guardar_datos(datos)
    assert not ok


def test_HU010_CA10_recuperacion_automatica_de_datos_tras_reinicio(app, monkeypatch):
    feed(monkeypatch, ["Usuario R", "r@dom.com", ""]) 
    app.crear_usuario()
    nuevo = StorageManager(app.storage.archivo_datos)
    assert len(nuevo.cargar_todos_usuarios()) == 1


def test_HU010_CA11_respaldo_facil_copiar_projects_json(app, monkeypatch, tmp_path):
    feed(monkeypatch, ["Usuario B", "b@dom.com", ""]) 
    app.crear_usuario()
    destino = tmp_path / "backup.json"
    shutil.copyfile(app.storage.archivo_datos, destino)
    assert destino.exists()


def test_HU010_CA12_recuperacion_elegante_json_corrupto(tmp_path):
    ruta = tmp_path / "data" / "projects.json"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text("{invalid json}", encoding="utf-8")
    sm = StorageManager(ruta)
    datos = sm.cargar_datos()
    assert datos == {"proyectos": [], "usuarios": []}