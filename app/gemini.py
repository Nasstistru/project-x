import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage  # Добавили SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=1
)

def get_ai_comment(expenses_list):
    if not expenses_list:
        return "Расходов пока нет, кошелек в безопасности!"

    expenses_text = ""
    for e in expenses_list:
        cat = getattr(e, 'category', 'Без категории')
        amt = getattr(e, 'amount', 0)
        expenses_text += f"- {cat}: {amt} грн.\n"

    system_instruction = SystemMessage(
        content=(
            "Ты — мудрый, но ироничный финансовый помощник. "
            "Твоя задача — анализировать список расходов пользователя. "
            "Пиши кратко (2-3 предложения), подколки приветствуются, но совет должен быть полезным. "
            "Отвечай строго на русском языке."
        )
    )

    user_message = HumanMessage(
        content=f"Вот мои расходы за сегодня:\n{expenses_text}\nЧто скажешь?"
    )

    try:
        res = model.invoke([system_instruction, user_message])
        return res.content
    except Exception as e:
        print(f"Ошибка при вызове Gemini: {e}")
        return "ИИ хотел что-то съязвить по поводу твоих трат, но у него пропал дар речи. Просто экономь!"



if __name__ == "__main__":
    print("Привет")