"""
EsSaludManager - Sistema de gestión para establecimientos de salud
Curso: Lenguajes de Programación
Fecha: 29 de septiembre de 2026
"""

import subprocess
import sys
from pathlib import Path

from src.gui.app import App


def inicializar_base_de_datos() -> bool:
    """
    Ejecuta el script de inicialización de la base de datos.

    Returns:
        bool: True si se creó correctamente, False si falló.
    """
    print("📦 Inicializando base de datos...")

    scripts_dir = Path(__file__).parent / "data" / "scripts"
    script_path = scripts_dir / "ejecutar_schema.py"

    if not script_path.exists():
        print("❌ Error: No se encontró ejecutar_schema.py")
        return False

    try:
        # Ejecutar script de inicialización
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            check=True,
        )

        print(result.stdout)

        if result.returncode == 0:
            print("✅ Base de datos inicializada correctamente.")
            return True
        else:
            print("❌ Error al inicializar la base de datos.")
            return False

    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(e.stderr)
        return False


def verificar_base_de_datos() -> bool:
    """
    Verifica que la base de datos exista.
    Si no existe, la crea automáticamente.

    Returns:
        bool: True si la BD existe o se creó, False si falló.
    """
    db_path = Path(__file__).parent / "data" / "esalud.db"

    if not db_path.exists():
        print("⚠️  Base de datos no encontrada.")
        print("   Iniciando creación automática...\n")

        if not inicializar_base_de_datos():
            return False

    return True


def main():
    """Punto de entrada de la aplicación"""
    print("=" * 50)
    print("EsSaludManager - Iniciando...")
    print("=" * 50)

    # Verificar/crear base de datos
    if not verificar_base_de_datos():
        print("\n❌ No se puede iniciar sin la base de datos.")
        print("   Solución manual: python data/scripts/ejecutar_schema.py")
        return

    # Iniciar aplicación
    app = App()
    app.run()


if __name__ == "__main__":
    main()
