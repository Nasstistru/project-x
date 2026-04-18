from datetime import date as Date
from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import HTMLResponse

# Твои внутренние инструменты
from app import crud
from app.schemas import ExpenseOut
from app.gemini import get_ai_comment  # Наша функция из gemini.py

router = APIRouter(tags=["expenses"])

# 1. Показываем главную страницу (интерфейс)
@router.get("/", response_class=HTMLResponse)
def ui():
    try:
        # Читаем HTML-файл
        with open("app/ui.html", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Файл ui.html не найден в папке app/")

# 2. Добавляем расход (POST запрос)
@router.post("/expenses", status_code=201)
def add_expense(
    amount:   float = Form(..., gt=0),
    category: str   = Form(..., min_length=1),
):
    # crud.create_expense теперь делает commit(), так что данные сохранятся
    new_expense = crud.create_expense(
        amount=amount,
        category=category,
        date=str(Date.today()),
    )
    return new_expense

# 3. Получаем расходы за дату + комментарий ИИ
@router.get("/expenses/{date}")
def list_expenses(date: str):
    # 1. Тянем данные из базы
    expenses = crud.get_expenses_by_date(date)

    # 2. Если пусто — сразу выкидываем 404
    if not expenses:
        raise HTTPException(status_code=404, detail=f"Расходов за {date} не найдено")

    # 3. Пытаемся получить мнение Gemini
    try:
        # Передаем список объектов ExpenseOut в нейронку
        ai_opinion = get_ai_comment(expenses)
    except Exception as e:
        print(f"Ошибка при связи с ИИ: {e}")
        ai_opinion = "ИИ временно вне зоны доступа, но ваши цифры в порядке."

    # 4. Возвращаем JSON с двумя полями: списком и текстом
    # FastAPI сам превратит объекты ExpenseOut в текст
    return {
        "expenses": expenses,
        "ai_comment": ai_opinion
    }