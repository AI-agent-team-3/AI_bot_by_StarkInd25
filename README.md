# 🏎️ Formula 1 RAG Bot & Security Suite

Комплексное решение для создания интеллектуального чат-бота на базе **RAG** (Retrieval-Augmented Generation) и проведения глубокого аудита безопасности (**Red Teaming**) языковых моделей. Бот специализируется на тематике «Формулы-1» и интегрирован с системами мониторинга и защиты.

## 📂 Структура проекта

```
.
├── bot.py                          # Основной бот (OpenRouter / GLM-4.5)
├── bot_local.py                    # Локальный бот (Ollama / Gemma 3)
├── rag.py                          # Логика векторного поиска (ChromaDB)
├── knowledge_base.txt              # База знаний о Формуле-1
├── web/                            # Исходный код сайта чат-бота
│
├── 🛡️ Модули безопасности (Security Suite)
│   ├── bot_security_eval.py        # Эвристический сканер (Jailbreak, Injection)
│   ├── deepteam_security_eval.py   # Авто-атаки и симуляция уязвимостей
│   ├── guardrails_bot_security.py  # Валидация через aka Guardrails
│
└── ⚙️ Инфраструктура
    ├── docker-compose.yml          # Стек мониторинга (Langfuse, DB, Redis)
    ├── requirements.txt            # Зависимости проекта
    └── .env                        # Переменные окружения (ключи API)


```

## 🚀 Быстрый старт

### 1. Установка окружения

Убедитесь, что у вас установлен Python 3.9+. Установите зависимости одной командой:

```
pip install -r requirements.txt


```


### 2. Настройка ключей (.env)

Создайте файл `.env` в корневой директории и заполните его:

```
BOT_TOKEN=ваш_токен_телеграм
OPENROUTER_API_KEY=ваш_ключ_openrouter
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=http://localhost:3000


```

### 3. Запуск инфраструктуры и бота

Для запуска основного скрипта бота:

```
python bot.py


```

Длая запуска сайта бота:

```
python -m uvicorn web.api:app --reload --port 8000

```
И пройдите по адресу в браузере http://localhost:8000

## 🧠 Технологический стек


|                    |                                                                                             |
| ------------------ | ------------------------------------------------------------------------------------------- |
| **Компонент**      | **Используемые технологии**                                                                 |
| **LLM**            | GLM-4.5-Air (через OpenRouter) или Gemma 3 (локально через Ollama)                          |
| **RAG**            | ChromaDB (RAM) · `paraphrase-multilingual-MiniLM-L12-v2` · `RecursiveCharacterTextSplitter` |
| **Observability**  | Langfuse — трейсинг вызовов, замер задержек, анализ «дерева мыслей»                         |
| **Инфраструктура** | Docker Compose (Langfuse, PostgreSQL, Redis)                                                |
| **Безопасность**   | Эвристические сканеры · ML-валидаторы  · DeepTeam                          |


## 🛡️ Аудит безопасности (Red Teaming)

Проект включает 4 независимых уровня проверки устойчивости бота. Результаты сохраняются в JSON-отчёты.


|                                   |                                                                                           |
| --------------------------------- | ----------------------------------------------------------------------------------------- |
| **Модуль**                        | **Назначение**                                                                            |
| `bot_security_eval.py`            | Базовые инъекции ("ignore instructions"), вредоносные советы (AdvBench) и утечка промпта. |
| `deepteam_security_eval.py`       | Симуляция сложных атак для выявления утечек секретных данных.                             |
| `guardrails_bot_security.py`      | ML‑фильтрация токсичности на выходе и детекция Jailbreak на входе.                        |   


**Запуск тестов:**

```
python bot_security_eval.py
python deepteam_security_eval.py
python guardrails_bot_security.py


```

## 📊 Мониторинг и отчётность

- **Langfuse UI:** Доступен по адресу `http://localhost:3000`. Позволяет анализировать «дерево мыслей», качество RAG и задержки.
- **JSON Reports:** Файлы (например, `security_eval_results.json`) содержат метрику **Pass Rate**, детализацию тестов и логи блокировок.
- **История диалогов:** Сохраняется локально в директории `conversations/` для аудита инцидентов.