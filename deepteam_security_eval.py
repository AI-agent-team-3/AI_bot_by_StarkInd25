import os
import json
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

from deepteam import red_team
from deepteam.vulnerabilities import PromptLeakage
from deepteam.attacks.single_turn import PromptInjection

# --- Настройки ---
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("❌ Не найден OPENROUTER_API_KEY в .env файле")

# OpenRouter
os.environ["OPENAI_API_KEY"] = OPENROUTER_API_KEY
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"
os.environ["OR_SITE_URL"] = "http://localhost"
os.environ["OR_APP_NAME"] = "TelegramF1Bot"

# Ваш бот
BOT_URL = "http://localhost:8000/chat"
RESULT_FILE = "deepteam_results.json"

class LocalBot:
    def generate(self, prompt: str) -> str:
        r = requests.post(
            BOT_URL,
            json={"user_id": 999, "message": prompt},
            timeout=120
        )
        r.raise_for_status()
        return r.json()["response"]

bot = LocalBot()

def model_callback(prompt: str) -> str:
    return bot.generate(prompt)

# --- МОДЕЛЬ GLM-4.5-Air ---
SIMULATOR_MODEL = "z-ai/glm-4.5-air:free"
EVALUATION_MODEL = "z-ai/glm-4.5-air:free"

# --- Тестирование ---
vulnerabilities = [
    PromptLeakage(types=["instructions"]),
    PromptLeakage(types=["secrets_and_credentials"]),
]

attacks = [
    PromptInjection(),
]

print(f"🚀 Запуск тестирования... Модель: {SIMULATOR_MODEL}")

risk_assessment = red_team(
    model_callback=model_callback,
    vulnerabilities=vulnerabilities,
    attacks=attacks,
    simulator_model=SIMULATOR_MODEL,
    evaluation_model=EVALUATION_MODEL,
    attacks_per_vulnerability_type=3,
    async_mode=False,
)

# --- Сохранение ---
output = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

if hasattr(risk_assessment, 'model_dump'):
    output["report"] = risk_assessment.model_dump()
elif hasattr(risk_assessment, 'dict'):
    output["report"] = risk_assessment.dict()
else:
    output["report"] = str(risk_assessment)

with open(RESULT_FILE, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False, default=str)

print(f"✅ Отчёт сохранён в: {RESULT_FILE}")