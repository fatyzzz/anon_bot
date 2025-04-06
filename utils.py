import uuid

def generate_unique_code() -> str:
    return str(uuid.uuid4())

def format_message(text: str) -> str:
    return f"<b>📨 Анонимное сообщение:</b>\n\n{text}"