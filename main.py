"""
EsSaludManager - Sistema de gestión para establecimientos de salud.

Curso: Lenguajes de Programación
Fecha: 29 de septiembre de 2026
"""

import subprocess
import sys
from pathlib import Path

from src.gui.app import App

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "data" / "esalud.db"
SCRIPT_PATH = BASE_DIR / "data" / "scripts" / "ejecutar_schema.py"


def inicializar_base_de_datos() -> bool:
    """
    Ejecuta el script de inicialización de la base de datos.

    Returns:
        True si la base de datos se creó correctamente.
    """
    print("📦 Inicializando base de datos...")

    if not SCRIPT_PATH.exists():
        print(f"❌ Error: No se encontró {SCRIPT_PATH}")
        return False

    try:
        resultado = subprocess.run(
            [sys.executable, str(SCRIPT_PATH)],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as error:
        print("❌ Error al inicializar la base de datos.")
        print(error.stderr)
        return False
    except OSError as error:
        print(f"❌ Error al ejecutar el script de inicialización: {error}")
        return False

    print(resultado.stdout)
    print("✅ Base de datos inicializada correctamente.")
    return True


def verificar_base_de_datos() -> bool:
    """
    Verifica que la base de datos exista.

    Si no existe, ejecuta la inicialización automática.

    Returns:
        True si la base de datos existe o fue creada.
    """
    if DB_PATH.exists():
        print(f"✅ Base de datos encontrada: {DB_PATH}")
        return True

    print("⚠️  Base de datos no encontrada.")
    print("   Iniciando creación automática...\n")

    return inicializar_base_de_datos()


def main() -> None:
    """Punto de entrada de la aplicación."""
    print("=" * 50)
    print("EsSaludManager - Iniciando...")
    print("=" * 50)

    if not verificar_base_de_datos():
        print("\n❌ No se puede iniciar sin la base de datos.")
        print("   Solución manual:")
        print("   python data/scripts/ejecutar_schema.py")
        return

    app = App()
    app.run()


if __name__ == "__main__":
    main()
