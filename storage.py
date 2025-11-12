import json
import os
from typing import List, Dict, Any, Optional
from models import Usuario, Proyecto, Tarea, Columna

class StorageManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.proyectos: List[Proyecto] = []
        self.usuarios: List[Usuario] = []
        self.usuario_actual_id: Optional[str] = None
        self.proyecto_actual_id: Optional[str] = None
        self.cargar_datos()

    def cargar_datos(self):
        if not os.path.exists(self.file_path):
            self.guardar_datos()
            return
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                self.usuarios = [Usuario.from_dict(u) for u in data.get('usuarios', [])]
                self.proyectos = [Proyecto.from_dict(p) for p in data.get('proyectos', [])]
                self.usuario_actual_id = data.get('usuario_actual_id')
                self.proyecto_actual_id = data.get('proyecto_actual_id')
        except (json.JSONDecodeError, FileNotFoundError):
            self.proyectos = []
            self.usuarios = []
            self.usuario_actual_id = None
            self.proyecto_actual_id = None

    def guardar_datos(self):
        data = {
            'usuarios': [u.to_dict() for u in self.usuarios],
            'proyectos': [p.to_dict() for p in self.proyectos],
            'usuario_actual_id': self.usuario_actual_id,
            'proyecto_actual_id': self.proyecto_actual_id
        }
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def guardar_usuario(self, usuario: Usuario):
        if any(u.email == usuario.email for u in self.usuarios):
            raise ValueError(f"El email '{usuario.email}' ya existe.")
        self.usuarios.append(usuario)
        self.guardar_datos()

    def set_usuario_actual(self, usuario_id: str):
        self.usuario_actual_id = usuario_id
        self.guardar_datos()

    def set_proyecto_actual(self, proyecto_id: str):
        self.proyecto_actual_id = proyecto_id
        self.guardar_datos()

    def cargar_todos_usuarios(self) -> list[Usuario]:
        return self.usuarios

    def eliminar_usuario(self, usuario_id: str):
        self.usuarios = [u for u in self.usuarios if u.usuario_id != usuario_id]
        self.guardar_datos()

    def guardar_proyecto(self, proyecto: Proyecto):
        self.proyectos.append(proyecto)
        self.guardar_datos()

    def cargar_todos_proyectos(self) -> list[Proyecto]:
        return self.proyectos

    def cargar_proyecto(self, proyecto_id: str) -> Optional[Proyecto]:
        for p in self.proyectos:
            if p.proyecto_id == proyecto_id:
                return p
        return None

    def eliminar_proyecto(self, proyecto_id: str):
        self.proyectos = [p for p in self.proyectos if p.proyecto_id != proyecto_id]
        self.guardar_datos()
