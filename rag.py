from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions

with open("knowledge_base.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Настройка "умного" сплиттера
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # целевой размер чанка (в символах, не токенах)
    chunk_overlap=100,  # перекрытие между чанками
    length_function=len,  # используем простое измерение по длине строки
    separators=[
        "\n\n", "\n", ".", "!", "?", ";", ":", ",", ".", "--"  # приоритетные границы
    ]
)

# Разделяем
# Разделяем
chunks = text_splitter.split_text(text)

# Для наглядности используем простые ID
ids = [str(i) for i in range(len(chunks))]

#print(f"Сами чанки: {chunks}")
#print(f"Количество чанков: {len(chunks)}")

# Создаём БД (в памяти)
client = chromadb.Client()

# Создаем русскоязычную embedding функцию
russian_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# Создаём коллекцию в БД
collection = client.create_collection("f1_history_guide", embedding_function=russian_ef)

# Добавляем документы из нашей базы знаний в коллекцию
collection.add(documents=chunks, ids=ids)

