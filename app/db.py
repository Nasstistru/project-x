import sqlite3
import os
from app.config import DB_PATH


def get_conn() -> sqlite3.Connection:
    # 1. Получаем путь к папке, где должна лежать база
    db_dir = os.path.dirname(DB_PATH)

    # 2. Создаем папку только если путь к ней не пустой
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        # Создаем таблицу, если её еще нет
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                amount      REAL    NOT NULL CHECK(amount > 0),
                category    TEXT    NOT NULL,
                date        TEXT    NOT NULL  -- формат YYYY-MM-DD
            )
        """)
        # Индекс ускоряет поиск, когда расходов станет очень много
        conn.execute("CREATE INDEX IF NOT EXISTS idx_date ON expenses(date)")
        conn.commit()


if __name__ == "__main__":
    init_db()
    print("База данных готова!")