# Plan de Pruebas - Biblioteca Municipal de San Gregorio

**Ámbito:** Solo pruebas unitarias.  
**Estado:** 100% de los tests unitarios pasan.

---

## Estrategia de Testing

- Únicamente tests unitarios sobre los modelos principales (`User`, `Activity`, `Enrollment`).
- Validación de reglas de negocio a bajo nivel (sin interacción HTTP o lógica de rutas/plantillas).
- Herramienta: pytest (con pytest.mark.unit).

---

## Matriz de Cobertura

| Modelo      | Funcionalidad Covered            | Probado |
|-------------|----------------------------------|---------|
| User        | Creación, password, rol          |   ✅    |
| Activity    | Creación, relaciones, status     |   ✅    |
| Enrollment  | Creación, duplicados, relación   |   ✅    |

---

## Casos de Prueba

### User
- Creación de usuario y asignación de datos
- Hashing y verificación de contraseña  
- Representación (__repr__)
- Asignación y validación de rol

### Activity
- Creación de actividad con datos válidos
- Estado por defecto
- Fechas y slots máximos
- Representación (__repr__)

### Enrollment
- Creación y validación de campos requeridos
- Relación con actividad y usuario  
- Evitar duplicados
- Representación (__repr__)
- Asignación correcta a actividad

---

## Criterios de Éxito

- Todos los tests unitarios deben ejecutarse correctamente con `pytest -m unit`.
- El código cubierto mínimamente: 80%+ sobre modelos.
- Sin tests de integración, funcionales ni de seguridad.

---

## Ejecución

```bash
pytest -m unit --cov=app --cov-report=term-missing
```

---

## Estado Actual

- **100% de tests unitarios pasan**
- Sin warnings ni errores de dependencias
- Sin tests de integración ni seguridad en el repo

---

## Guía para Nuevos Tests

Agrega archivos en `tests/unit/` y usa el decorador:
```python
@pytest.mark.unit
def test_mi_funcionalidad():
    # tu test...
```

---

## Historial

- Febrero 2026: Refactor para dejar solo tests unitarios.
- Mayo 2025-Enero 2026: Incorpora integración y seguridad (archivado, NO activo).

---
