from pathlib import Path

import psycopg2

from src.config import DATABASE_CONFIG



def init_db():
    # Locate the project root.
    project_root= Path(__file__).resolve().parent.parent

    # Locate and read the SQL schema file.
    schema_path = project_root / "sql" / "schema.sql"
    schema_sql = schema_path.read_text(encoding="utf-8")

    # Connect to PostgreSQL.
    conn = psycopg2.connect(**DATABASE_CONFIG)

    try:
        # Execute the SQL schema.
        with conn.cursor() as cur:
            cur.execute(schema_sql)

        # Save the transaction.
        conn.commit()

        print("Database schema initialized successfully.")

    finally:
        # Always close the database connection.
        conn.close()

if __name__ == "__main__":
    init_db()