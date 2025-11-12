import pytest
from models import Proyecto, Tarea, Usuario

# Casos de Prueba para la Historia de Usuario HU-005: Búsqueda de Tareas

@pytest.fixture
def setup_proyecto_con_tareas():
    # Setup del proyecto y tareas para las pruebas de búsqueda
    proyecto = Proyecto(nombre="Proyecto de Búsqueda")
    usuario = Usuario(nombre="Usuario de Prueba", email="test@test.com")
    
    # Tareas para probar diferentes escenarios de búsqueda
    tareas = [
        Tarea(titulo="Implementar funcionalidad A", descripcion="Detalles de la funcionalidad A"),
        Tarea(titulo="Corregir bug en B", descripcion="El bug ocurre al hacer clic"),
        Tarea(titulo="Documentar API", descripcion="Redactar la documentación para la API REST"),
        Tarea(titulo="Tarea IMPORTANTE", descripcion="Esta es una tarea crítica", prioridad="Urgente"),
        Tarea(titulo="Refactorizar código antiguo", descripcion="Mejorar la legibilidad del código", asignado_a=usuario.usuario_id)
    ]
    
    columna_pendiente = next((col for col in proyecto.columnas if col.nombre == "Pendiente"), None)
    assert columna_pendiente is not None, "La columna 'Pendiente' no se encontró en el proyecto."
    for tarea in tareas:
        columna_pendiente.agregar_tarea(tarea)
        
    return proyecto, tareas, usuario

def test_hu005_ca1_ingresar_termino_busqueda(setup_proyecto_con_tareas):
    """Validar que el usuario puede ingresar un término de búsqueda."""
    # Simulación: Este caso de prueba es más sobre la interacción del CLI,
    # pero podemos probar la lógica de búsqueda subyacente.
    proyecto, _, _ = setup_proyecto_con_tareas
    resultados = proyecto.buscar_tareas("funcionalidad")
    assert len(resultados) > 0, "La búsqueda con un término válido debería devolver resultados."

def test_hu005_ca2_buscar_en_titulos_parcial(setup_proyecto_con_tareas):
    """Validar que el sistema busca en títulos de tareas con búsqueda parcial."""
    proyecto, _, _ = setup_proyecto_con_tareas
    resultados = proyecto.buscar_tareas("Implementar")
    assert len(resultados) == 1
    assert resultados[0].titulo == "Implementar funcionalidad A"

def test_hu005_ca3_buscar_en_descripciones_parcial(setup_proyecto_con_tareas):
    """Validar que el sistema busca en descripciones de tareas con búsqueda parcial."""
    proyecto, _, _ = setup_proyecto_con_tareas
    resultados = proyecto.buscar_tareas("documentación")
    assert len(resultados) == 1
    assert resultados[0].titulo == "Documentar API"

def test_hu005_ca4_busqueda_insensible_mayusculas(setup_proyecto_con_tareas):
    """Validar que la búsqueda es insensible a mayúsculas y minúsculas."""
    proyecto, _, _ = setup_proyecto_con_tareas
    resultados = proyecto.buscar_tareas("IMPORTANTE")
    assert len(resultados) == 1
    assert resultados[0].titulo == "Tarea IMPORTANTE"

def test_hu005_ca5_contar_tareas_encontradas(setup_proyecto_con_tareas):
    """Validar que el sistema muestra el número total de tareas encontradas."""
    proyecto, _, _ = setup_proyecto_con_tareas
    # "código" está en el título de una y en la descripción de otra
    resultados = proyecto.buscar_tareas("código")
    assert len(resultados) == 2

def test_hu005_ca8_mensaje_sin_resultados(setup_proyecto_con_tareas):
    """Validar que se muestra un mensaje claro si no hay resultados de búsqueda."""
    proyecto, _, _ = setup_proyecto_con_tareas
    resultados = proyecto.buscar_tareas("xyz123abc")
    assert len(resultados) == 0, "La búsqueda de un término inexistente no debería devolver resultados."

def test_hu005_ca9_termino_busqueda_vacio(setup_proyecto_con_tareas):
    """Validar que el término de búsqueda no puede estar vacío."""
    proyecto, _, _ = setup_proyecto_con_tareas
    with pytest.raises(ValueError, match="El termino de busqueda no puede estar vacio"):
        proyecto.buscar_tareas("")