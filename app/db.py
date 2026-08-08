import os
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "incident_manager"),
        user=os.getenv("DB_USER", "incident_user"),
        password=os.getenv("DB_PASSWORD"),
        row_factory=dict_row,
    )


@contextmanager
def db_cursor():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            yield cursor

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
