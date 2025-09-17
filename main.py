# MODULO: ROOT.
# .. ................................................................. main ..󰌠
"""Punto de entrada principal para la aplicación de Tareas-CLI.

Este script es el responsable de inicializar y ejecutar la interfaz de
usuario de la aplicación.
"""
from controllers.interface import Interface


def main() -> None:
    """Inicializa y ejecuta la aplicación.

    Crea una instancia de la clase Interface y llama a su método de ejecución
    principal para poner en marcha el bucle de la aplicación.
    """
    app = Interface()
    app.run()



if __name__ == "__main__":
    main()
