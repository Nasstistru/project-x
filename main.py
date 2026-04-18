from fastapi import FastAPI
from app.db import init_db
from app.routes import router

# Создаем само приложение
app = FastAPI(
    title="Мимими",
    description="Учёт расходов по категориям и датам",
    version="1.0.0"
)

# Запускаем базу данных (создаем таблицу, если её нет)
@app.on_event("startup")
def startup_event():
    init_db()

# Подключаем все наши пути из routes.py
app.include_router(router)

# Этот блок позволяет запускать файл напрямую через Python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)