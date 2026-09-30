#!/usr/bin/env python3
"""
Script para inicializar la base de datos de EsSaludManager.

Uso:
    python ejecutar_schema.py [--reset] [--test]

Opciones:
    --reset   Eliminar BD existente antes de crear
    --test    Crear BD de pruebas (test_esalud.db)
"""

import argparse
import sqlite3
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent  # data/
SCRIPTS_DIR = Path(__file__).parent  # data/scripts/
SQL_CREATE = SCRIPTS_DIR / "create_tables.sql"
SQL_INSERT = SCRIPTS_DIR / "insert_initial_data.sql"


def ejecutar_sql(conn: sqlite3.Connection, sql_file: Path) -> None:
    """Ejecuta un archivo SQL en la conexión dada."""
    if not sql_file.exists():
        raise FileNotFoundError(f"❌ Archivo SQL no encontrado: {sql_file}")

    with open(sql_file, "r", encoding="utf-8") as f:
        sql_script = f.read()

    conn.executescript(sql_script)
    conn.commit()


def crear_base_de_datos(db_path: Path, reset: bool = False) -> None:
    """Crea la base de datos desde los scripts SQL."""

    # Verificar si ya existe
    if db_path.exists():
        if reset:
            print(f"🗑️  Eliminando {db_path}...")
            db_path.unlink()
        else:
            print(f"⚠️  {db_path} ya existe. Usa --reset para sobrescribir.")
            return

    # Crear directorio si no existe
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Conectar y ejecutar scripts
    print(f"📦 Creando {db_path}...")
    conn: sqlite3.Connection = sqlite3.connect(str(db_path))

    try:
        # 1. Crear tablas e índices
        print("📋 Ejecutando create_tables.sql...")
        ejecutar_sql(conn, SQL_CREATE)
        print("✅ Tablas e índices creados.")

        # 2. Insertar datos iniciales
        print("📋 Ejecutando insert_initial_data.sql...")
        ejecutar_sql(conn, SQL_INSERT)
        print("✅ Datos iniciales insertados.")

    except sqlite3.Error as e:
        print(f"❌ Error de SQLite: {e}")
        # Rollback: eliminar BD corrupta
        if db_path.exists():
            db_path.unlink()
            print(f"🗑️  {db_path} eliminada (rollback).")
        raise

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        raise

    finally:
        conn.close()

    print(f"✨ {db_path} creada exitosamente.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inicializar BD de EsSaludManager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
    python ejecutar_schema.py              # Crear esalud.db
    python ejecutar_schema.py --reset      # Recrear esalud.db
    python ejecutar_schema.py --test       # Crear test_esalud.db
    python ejecutar_schema.py --reset --test  # Recrear test_esalud.db
        """,
    )
    parser.add_argument(
        "--reset", action="store_true", help="Eliminar BD existente antes de crear"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Crear BD de pruebas (test_esalud.db) en lugar de esalud.db",
    )

    args = parser.parse_args()

    # Determinar nombre de BD
    if args.test:
        db_path = BASE_DIR / "test_esalud.db"
    else:
        db_path = BASE_DIR / "esalud.db"

    # Crear BD
    crear_base_de_datos(db_path, reset=args.reset)

    print("\n✅ Base de datos lista.")


if __name__ == "__main__":
    main()
