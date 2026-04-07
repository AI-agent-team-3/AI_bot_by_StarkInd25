import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Импортируем любую версию бота, например bot_local или bot
from bot import llm, sanitize_output, SYSTEM_PROMPT, get_rag_context, load_user_history, append_to_user_history_file
#from bot_local import llm, sanitize_output, SYSTEM_PROMPT, get_rag_context, load_user_history, append_to_user_history_file

load_dotenv()

app = FastAPI(title="F1 Chat API")

# CORS чтобы фронтенд мог делать POST
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Статика
app.mount("/static", StaticFiles(directory="web/static"), name="static")


@app.get("/")
async def root():
    """Возвращает index.html"""
    with open("web/static/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/chat")
async def chat_endpoint(request: Request):
    """
    Универсальный endpoint для чата.
    Использует LLM и RAG из импортированного бота.
    """
    try:
        data = await request.json()
        user_id = int(data.get("user_id", 1))
        user_text = data.get("message", "")

        # Загружаем историю пользователя
        history = load_user_history(user_id)

        # Собираем контекст
        context_lines = []
        for pair in history:
            context_lines.append(f"User: {pair['user']}")
            context_lines.append(f"Assistant: {pair['assistant']}")
        context_lines.append(f"User: {user_text}")
        dialog_context = "\n".join(context_lines)[-3000:]

        # Получаем RAG
        rag_context = get_rag_context(user_text)

        final_prompt = f"{SYSTEM_PROMPT}\n\nRAG:\n{rag_context}\n\n{dialog_context}"

        # Генерация LLM
        llm_result = llm.invoke(final_prompt)
        response_text = getattr(llm_result, "content", str(llm_result))
        response_text = sanitize_output(response_text)

        # Сохраняем в историю
        history.append({"user": user_text, "assistant": response_text})
        append_to_user_history_file(user_id, user_text, response_text)

        return JSONResponse({"response": response_text})

    except Exception as e:
        return JSONResponse({"response": f"Ошибка: {str(e)}"})