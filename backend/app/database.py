import os
from sqlalchemy import create_engine, text
from contextlib import contextmanager


def get_db_connection_string():
    user = os.environ.get("POSTGRES_USER", "ascentris")
    password = os.environ.get("POSTGRES_PASSWORD", "Ascentris2023")
    host = os.environ.get("POSTGRES_HOST", "postgres")
    port = os.environ.get("POSTGRES_PORT", "5432")
    db = os.environ.get("POSTGRES_DB", "ascentris_db")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


engine = create_engine(get_db_connection_string(), pool_pre_ping=True)


@contextmanager
def get_connection():
    """Context manager for database connections."""
    conn = engine.connect()
    try:
        yield conn
    finally:
        conn.close()


def get_table_row_counts():
    """Return row counts for all expected tables (for health check)."""
    tables = [
        "raw_Daily", "raw_Monthly", "raw_Quarterly",
        "Daily", "Monthly", "Quarterly",
        "CPIWeightedChange",
    ]
    counts = {}
    with get_connection() as conn:
        for table in tables:
            try:
                result = conn.execute(text(f'SELECT COUNT(*) FROM "{table}"'))
                counts[table] = result.scalar()
            except Exception:
                counts[table] = None
    return counts
