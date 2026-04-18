from app.db import get_conn
from app.schemas import ExpenseOut


def create_expense(amount: float, category: str, date: str) -> ExpenseOut:
    with get_conn() as conn:
        # Сохраняем данные в таблицу
        cursor = conn.execute(
            "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
            (amount, category, date),
        )
        conn.commit()  # ОБЯЗАТЕЛЬНО фиксируем изменения в базе

        # Возвращаем созданный объект
        return ExpenseOut(
            id=cursor.lastrowid,
            amount=amount,
            category=category,
            date=date
        )


def get_expenses_by_date(date: str) -> list[ExpenseOut]:
    with get_conn() as conn:
        # Достаем все записи за конкретное число
        rows = conn.execute(
            "SELECT id, amount, category, date FROM expenses WHERE date = ? ORDER BY id",
            (date,),
        ).fetchall()

        # Превращаем каждую строку из базы в объект ExpenseOut
        expenses = []
        for row in rows:
            expenses.append(ExpenseOut(
                id=row[0],
                amount=row[1],
                category=row[2],
                date=row[3]
            ))
        return expenses