import os
import psycopg2
from psycopg2.extras import RealDictCursor

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "textai_db")
DB_USER = os.getenv("POSTGRES_USER", "spostgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "psql123")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        cursor_factory=RealDictCursor
    )

def save_analysis(user_id, input_text, analysis_type, result):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO text_analysis (user_id, input_text, analysis_type, result)
                VALUES (%s, %s, %s, %s)
                RETURNING id, created_at;
                """,
                (user_id, input_text, analysis_type, result)
            )
            row = cur.fetchone()
            conn.commit()
            return row
    finally:
        conn.close()
