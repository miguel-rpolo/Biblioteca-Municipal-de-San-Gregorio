# Tests Unitarios - Biblioteca Municipal de San Gregorio

Este repositorio contiene únicamente **tests unitarios** para el sistema de actividades de la Biblioteca Municipal de San Gregorio.

## Estructura

```
tests/
├── __init__.py
├── conftest.py
├── pytest.ini
├── unit/
│   ├── __init__.py
│   ├── test_user_model.py
│   ├── test_activity_model.py
│   └── test_enrollment_model.py
└── README.md  # Este archivo
```

## ¿Qué se prueba?

- **Modelos principales** (`User`, `Activity`, `Enrollment`):
    - Creación de instancias, relaciones, funcionalidades básicas de negocio.
    - Métodos: `set_password`, `check_password`, `__repr__`, asignación de roles, campos requeridos.
    - Validación de duplicados y de campos.

## Ejecución

Instala dependencias de desarrollo:
```bash
pip install -r requirements-dev.txt
```

Ejecuta solo los tests unitarios:
```bash
pytest -m unit -v
```

## Añadir nuevos tests

Crea/modifica archivos dentro de `tests/unit/`. Usa el decorador `@pytest.mark.unit`. Ejemplo:
```python
import pytest

@pytest.mark.unit
class TestMiUnidad:
    def test_algo(self):
        assert 1 + 1 == 2
```

## Cobertura

Para ver cobertura de los tests:
```bash
pytest --cov=app --cov-report=term-missing -m unit
```

## Estado actual

- **Cobertura**: Modelos principales.
- **Status**: TODOS los tests unitarios pasan.
- **Sin tests de integración ni seguridad**.

## Plan de pruebas

Consulta `docs/Plan_de_Pruebas_Completo.md` para el plan actualizado de pruebas unitarias.
