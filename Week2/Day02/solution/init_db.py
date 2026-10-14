import argparse
from pathlib import Path

import psycopg
from psycopg import sql

from database import settings
from data_loader import DEFAULT_CSV_PATH, load_csv


BASE_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = BASE_DIR / "schema.sql"


def maintenance_url(database_name: str = "postgres") -> str:
    return (
        f"postgresql://{settings.db_user}:{settings.db_password}"
        f"@{settings.db_host}:{settings.db_port}/{database_name}"
    )


def ensure_database_exists() -> None:
    with psycopg.connect(maintenance_url(), autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (settings.db_name,),
            )
            exists = cur.fetchone()
            if exists:
                print(f"Database already exists: {settings.db_name}")
                return

            cur.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(settings.db_name),
                )
            )
            print(f"Created database: {settings.db_name}")


def apply_schema() -> None:
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    with psycopg.connect(settings.database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(schema_sql)
        conn.commit()
    print(f"Applied schema from: {SCHEMA_PATH}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create database, apply schema, and load sample data.")
    parser.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV_PATH,
        help="CSV file to load after schema creation.",
    )
    parser.add_argument(
        "--skip-load",
        action="store_true",
        help="Only create database and schema; do not load CSV data.",
    )
    args = parser.parse_args()

    ensure_database_exists()
    apply_schema()

    if not args.skip_load:
        loaded = load_csv(args.csv)
        print(f"Loaded {loaded} encounters from {args.csv}")


if __name__ == "__main__":
    main()

