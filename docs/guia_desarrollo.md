# Guía de Desarrollo

Esta guía está destinada a desarrolladores que deseen contribuir al proyecto, o para configurar el entorno de desarrollo desde cero.

## 1. Requisitos Previos

-   Python 3.11 o superior.
-   `uv`: Un instalador y gestor de paquetes de Python extremadamente rápido, escrito en Rust. Si no lo tienes, puedes instalarlo
      siguiendo las [instrucciones oficiales](https://github.com/astral-sh/uv).

## 2. Configuración del Entorno

Sigue estos pasos para tener un entorno de desarrollo funcional:

### a. Clonar el Repositorio
```bash
  git clone https://github.com/Gustavo9481/Tasks-cli.git
  cd Tasks-cli
```

### b. Crear el Entorno Virtual

Usamos `uv` para crear y gestionar el entorno virtual. Esto asegura que las dependencias del proyecto estén aisladas.
```bash
  uv venv
```

Este comando creará una carpeta `.venv` en la raíz del proyecto y la activará automáticamente en tu sesión de terminal actual.

### c. Instalar Dependencias

Todas las dependencias necesarias para el desarrollo (incluyendo las de producción) se encuentran en el archivo `pyproject.toml`.

```bash
  uv pip install ".[dev]"
```


## 3. Herramientas de Calidad de Código

Este proyecto utiliza un conjunto de herramientas para mantener un código limpio, consistente y libre de errores comunes. Es recomendable ejecutarlas antes de hacer un `commit`.

### a. Formateo de Código y Linter.

`ruff` es un formateador de código "testarudo" que asegura un estilo consistente en todo el proyecto.
```bash
  uv run ruff check .
```

### b. Verificación de Tipos (Mypy)

`mypy` es un verificador de tipos estático. Revisa las anotaciones de tipo para prevenir errores comunes antes de que el código se ejecute.
```bash
  uv run mypy .
```

## 4. Ejecución de Pruebas (Pytest)

Las pruebas son una parte fundamental del proyecto y se utilizan para verificar
que la lógica de negocio y el acceso a datos funcionan como se espera.

Para ejecutar todo el conjunto de pruebas:

```bash
  uv run pytest
```

## 5. Ejecución de la Aplicación en Modo Desarrollo

Para correr la aplicación principal:
  python main.py
*(Nota: Asegúrate de que el archivo principal se llame `main.py` o ajusta el comando según corresponda).*
