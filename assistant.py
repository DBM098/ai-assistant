from groq import Groq
from config import MODEL, MAX_TOKENS, SYSTEM_PROMPT


class AIAssistant:
    def __init__(self):
        self.client = Groq()
        self.history = []

    def chat(self, user_message: str) -> str:
        """Envía un mensaje y obtiene una respuesta del asistente."""
        self.history.append({"role": "user", "content": user_message})

        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + self.history

        response = self.client.chat.completions.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=messages,
        )

        assistant_message = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": assistant_message})
        return assistant_message

    def reset(self):
        """Reinicia el historial de conversación."""
        self.history = []
        print("🔄 Conversación reiniciada.\n")
