from pydantic import BaseModel, Field, ConfigDict

# Схема для создания (то, что мы получаем от пользователя)
class ExpenseCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Сумма расхода, должна быть > 0")
    category: str = Field(..., min_length=1, description="Категория расхода")

# Схема для вывода (то, что мы отправляем на фронтенд)
class ExpenseOut(BaseModel):
    id: int
    amount: float
    category: str
    date: str

    # Эта настройка позволяет Pydantic работать с объектами из базы данных
    model_config = ConfigDict(from_attributes=True)