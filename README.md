# Biblioteca Municipal de San Gregorio · Sistema de Gestión

Sistema web para gestión de actividades, inscripciones y administración de la Biblioteca Municipal de San Gregorio.

---

## Documentos base del proyecto

La documentación completa y los documentos funcionales y de requisitos se encuentran en la carpeta [`docs/`](./docs):

- [Plan de Pruebas Completo](./docs/Plan_de_Pruebas_Completo.md)
- [Análisis funcional y requisitos](./docs/Analisis_funcional_y_requisitos.pdf)
- [Historias de usuario](./docs/Historias_de_usuario.pdf)
- [Problema del cliente](./docs/Problema%20del%20cliente.txt)
- [Propuesta tecnológica y diseño técnico](./docs/Propuesta_tecnolgica_y_diseno_tecnico.pdf)

---

## Quickstart

### Ejecución automática para desarrollo

Utiliza el siguiente comando en la raíz del proyecto (Windows):

```cmd
call run_all.bat
```

Esto instala dependencias, prepara la base de datos y ejecuta la aplicación automáticamente.  
Si el sistema ya está instalado, simplemente lanzará la aplicación con los datos de prueba.

> Si ves advertencias de permisos, usa un terminal tipo **"Símbolo del sistema"** o **"PowerShell"** con permisos normales.

---

### Pasos detallados (opcional)

1. Prepara entorno virtual y dependencias:

    ```bash
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    ```

2. Configura la base de datos y seed:

    ```bash
    python migrate_db.py
    python seed_data.py
    ```

3. Lanza la aplicación:

    ```bash
    python run.py
    ```
    - Accede a http://localhost:5000

4. Prueba los tests unitarios (opcional):

    ```bash
    pytest -m unit -v
    ```

---

## Capturas de pantalla

A continuación se muestran capturas reales del sistema corriendo:

<div align="center">

<img alt="Login" src="docs/screenshots/Captura%20de%20pantalla%202026-02-27%20110932.png" width="490"/>

<img alt="Listado de actividades" src="docs/screenshots/Captura%20de%20pantalla%202026-02-27%20110958.png" width="490"/>

<img alt="Detalle de actividad" src="docs/screenshots/Captura%20de%20pantalla%202026-02-27%20111019.png" width="490"/>

<img alt="Dashboard admin" src="docs/screenshots/Captura%20de%20pantalla%202026-02-27%20111030.png" width="490"/>

<img alt="Formulario nueva actividad" src="docs/screenshots/Captura%20de%20pantalla%202026-02-27%20111051.png" width="490"/>

</div>

---

## Resumen de arquitectura y diseño

### Tecnologías principales

- **Flask**: Web framework ligero.
- **SQLAlchemy**: ORM para persistencia.
- **Jinja2**: Plantillas HTML.
- **pytest**: Pruebas unitarias.

### Principales módulos

- `app/models/`: Modelos principales (`User`, `Activity`, `Enrollment`) y relaciones.
- `app/routes/`: Blueprints para rutas de autenticación, actividades y administración.
- `app/templates/`: Plantillas Jinja2 organizadas por área.
- `tests/unit/`: Pruebas unitarias de lógica de negocio y modelos.
- `memory-bank/`: Documentación viva de contexto y patrones arquitectónicos.
- `docs/`: Documentación de alto nivel, requisitos y anexos técnicos.

### Diseño y patrones

- **MVC simplificado:** Separación entre modelos, vistas (plantillas) y lógica (rutas/controllers).
- **Blueprints:** Rutas desacopladas según contexto.
- **Configurable:** Soporte a entornos, base de datos y extensiones.
- **Testing first:** Modelo robusto de pruebas unitarias desde el inicio.

---

## Cómo contribuir

1. Lee [docs/Analisis_funcional_y_requisitos.pdf](./docs/Analisis_funcional_y_requisitos.pdf)
2. Haz fork y crea una rama para tus cambios.
3. Añade/ajusta pruebas si es relevante.
4. Haz un pull request.

---
