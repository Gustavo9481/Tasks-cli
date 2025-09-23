# Guía de Usuario

¡Bienvenido a Tasks-cli ! Esta guía te mostrará cómo instalar y utilizar la aplicación para gestionar tus tareas directamente desde la terminal.

## 1. Instalación

Para utilizar la aplicación, necesitas tener **Python 3.11** o una versión superior instalada en tu sistema.

Sigue estos sencillos pasos:

### a. Descarga del Proyecto

Primero, descarga el código fuente. Puedes hacerlo clonando el repositorio
con `git`:
```bash
  git clone https://github.com/Gustavo9481/Tasks-cli.git
  cd Tasks-cli
```

O descargando el archivo ZIP directamente desde GitHub.

### b. Instalación de Dependencias

La aplicación utiliza algunas librerías de Python que deben ser instaladas. 
La forma más sencilla es usando `uv` (o `pip`) y el archivo `pyproject.toml`.

Crea el entorno virtual
```bash
  uv venv
```
Instalar las dependencias
```bash
  uv pip install ".[dev]"
```

## 2. Ejecución de la Aplicación

Una vez instaladas las dependencias, puedes iniciar la aplicación ejecutando el
siguiente comando desde la carpeta raíz del proyecto:
```bash
  tasks-cli
```

*(Nota: El archivo principal debe llamarse `main.py` o el comando debe 
ajustarse al nombre correcto).*

Al ejecutarlo, verás la interfaz principal con tu lista de tareas.

## 3. Funcionalidades y Atajos de Teclado

La interfaz es completamente interactiva y se maneja con atajos de teclado. 
La tabla de tareas se puede navegar con las **flechas arriba y abajo**.

Aquí tienes la lista de acciones disponibles:

| Tecla | Acción               | Descripción                                          |
| :---- | :------------------- | :--------------------------------------------------- |
| **n** | **Nueva Tarea**      | Abre un formulario para crear una nueva tarea.       |
| **e** | **Editar Tarea**     | Editar una tarea ingresando el ID.                   |
| **d** | **Eliminar Tarea**   | Eliminar uns tarea ingresando el ID.                 |
| **m** | **Marcar/Desmarcar** | Cambiar el status de una tarea ingresando ID.        |
| **v** | **Ver Detalles**     | Ver los detalles o anotaciones extras ingresando ID. |
| **f** | **Filtrar Tareas**   | Filtrar tareas por status, tag o prioridad.          |
| **r** | **Refrescar Tareas** | Actualizar la lista de tareas.                       |
| **q** | **Salir**            | Cierra laaplicación.                                 |

¡Y eso es todo! Con estos comandos puedes gestionar tus tareas de forma rápida 
y eficiente sin salir de tu terminal.
