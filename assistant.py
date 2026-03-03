import anthropic
from config import MODEL, MAX_TOKENS, SYSTEM_PROMPT


class AIAssistant:
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.history = []

    def chat(self, user_message: str) -> str:
        """Envía un mensaje y obtiene una respuesta del asistente."""
        self.history.append({"role": "user", "content": user_message})

        response = self.client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=self.history,
        )

        assistant_message = response.content[0].text
        self.history.append({"role": "assistant", "content": assistant_message})
        return assistant_message

    def reset(self):
        """Reinicia el historial de conversación."""
        self.history = []
        print("🔄 Conversación reiniciada.\n")
