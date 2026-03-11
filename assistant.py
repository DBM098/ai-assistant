import os
import base64
import requests
from groq import Groq
from config import MODEL, VISION_MODEL, MAX_TOKENS, SYSTEM_PROMPT

TAVILY_KEY = os.environ.get("TAVILY_API_KEY", "")


def web_search(query: str) -> str:
    try:
        res = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": TAVILY_KEY,
                "query": f"{query} Mexico",
                "max_results": 5,
                "search_depth": "advanced",
            },
            timeout=8,
        )
        data = res.json()
        results = []
        for r in data.get("results", []):
            results.append(f"- {r['title']}: {r['content'][:200]}")
        return "\n".join(results) if results else "Sin resultados."
    except Exception as e:
        return f"Error al buscar: {e}"


SYSTEM_WITH_SEARCH = SYSTEM_PROMPT + """

Tienes acceso a busqueda web en tiempo real. Cuando el ser superior pregunte sobre
librerias, frameworks, documentacion o cualquier informacion actualizada de programacion,
usa los resultados de busqueda incluidos en el mensaje para responder."""


class AIAssistant:
    def __init__(self):
        self.client = Groq()
        self.history = []

    def needs_search(self, message: str) -> bool:
        keywords = [
            "hoy", "ahora", "actual", "reciente", "ultimo", "ultimos",
            "noticias", "precio", "clima", "tiempo", "2024", "2025", "2026",
            "quien gano", "que paso", "nueva", "nuevo", "version", "update"
        ]
        return any(k in message.lower() for k in keywords)

    def chat(self, user_message: str) -> str:
        enriched = user_message
        if self.needs_search(user_message):
            search_results = web_search(user_message)
            enriched = f"{user_message}\n\n[RESULTADOS WEB:\n{search_results}]"

        self.history.append({"role": "user", "content": enriched})
        messages = [{"role": "system", "content": SYSTEM_WITH_SEARCH}] + self.history

        response = self.client.chat.completions.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=messages,
        )

        reply = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def analyze_image(self, image_bytes: bytes, user_message: str) -> str:
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        response = self.client.chat.completions.create(
            model=VISION_MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
                    },
                    {
                        "type": "text",
                        "text": user_message if user_message else "Describe esta imagen, lee cualquier texto que veas y si hay codigo, explicalo."
                    }
                ]
            }]
        )
        return response.choices[0].message.content

    def reset(self):
        self.history = []