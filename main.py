from flask import Flask, request, jsonify, render_template_string
from assistant import AIAssistant

app = Flask(__name__)
assistant = AIAssistant()

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Asistente IA</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, sans-serif;
      background: #0f0f0f;
      color: #fff;
      height: 100vh;
      display: flex;
      flex-direction: column;
    }
    header {
      padding: 16px 20px;
      background: #1a1a1a;
      border-bottom: 1px solid #333;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    header h1 { font-size: 18px; }
    header span { font-size: 22px; }
    #chat {
      flex: 1;
      overflow-y: auto;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .msg {
      max-width: 75%;
      padding: 12px 16px;
      border-radius: 18px;
      line-height: 1.5;
      font-size: 15px;
      white-space: pre-wrap;
    }
    .user {
      background: #2f6df5;
      align-self: flex-end;
      border-bottom-right-radius: 4px;
    }
    .ai {
      background: #1e1e1e;
      align-self: flex-start;
      border-bottom-left-radius: 4px;
      border: 1px solid #333;
    }
    .typing {
      background: #1e1e1e;
      align-self: flex-start;
      border-bottom-left-radius: 4px;
      border: 1px solid #333;
      padding: 12px 16px;
      border-radius: 18px;
    }
    .dot { display: inline-block; width: 8px; height: 8px; background: #888; border-radius: 50%; margin: 0 2px; animation: bounce 1s infinite; }
    .dot:nth-child(2) { animation-delay: 0.2s; }
    .dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes bounce { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-6px)} }
    #form {
      padding: 16px 20px;
      background: #1a1a1a;
      border-top: 1px solid #333;
      display: flex;
      gap: 10px;
    }
    #input {
      flex: 1;
      padding: 12px 16px;
      border-radius: 24px;
      border: 1px solid #444;
      background: #2a2a2a;
      color: #fff;
      font-size: 15px;
      outline: none;
    }
    #input:focus { border-color: #2f6df5; }
    button {
      padding: 12px 20px;
      background: #2f6df5;
      color: #fff;
      border: none;
      border-radius: 24px;
      font-size: 15px;
      cursor: pointer;
    }
    button:active { background: #1a55d4; }
    #reset {
      background: transparent;
      border: 1px solid #444;
      color: #aaa;
      padding: 8px 14px;
      font-size: 13px;
    }
  </style>
</head>
<body>
  <header>
    <span>🤖</span>
    <h1>Asistente IA</h1>
    <button id="reset" onclick="resetChat()">↺ Reiniciar</button>
  </header>

  <div id="chat">
    <div class="msg ai">¡Hola! Soy ChIAquil. ¿En qué puedo ayudarte hoy?</div>
  </div>

  <div id="form">
    <input id="input" type="text" placeholder="Escribe tu mensaje..." autocomplete="off" />
    <button onclick="sendMessage()">Enviar</button>
  </div>

  <script>
    const chat = document.getElementById('chat');
    const input = document.getElementById('input');

    input.addEventListener('keydown', e => { if (e.key === 'Enter') sendMessage(); });

    function addMsg(text, who) {
      const div = document.createElement('div');
      div.className = 'msg ' + who;
      div.textContent = text;
      chat.appendChild(div);
      chat.scrollTop = chat.scrollHeight;
      return div;
    }

    function showTyping() {
      const div = document.createElement('div');
      div.className = 'typing';
      div.id = 'typing';
      div.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
      chat.appendChild(div);
      chat.scrollTop = chat.scrollHeight;
    }

    function hideTyping() {
      const t = document.getElementById('typing');
      if (t) t.remove();
    }

    async function sendMessage() {
      const text = input.value.trim();
      if (!text) return;
      input.value = '';
      addMsg(text, 'user');
      showTyping();

      try {
        const res = await fetch('/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        hideTyping();
        addMsg(data.response, 'ai');
      } catch {
        hideTyping();
        addMsg('❌ Error al conectar. Intenta de nuevo.', 'ai');
      }
    }

    async function resetChat() {
      await fetch('/reset', { method: 'POST' });
      chat.innerHTML = '<div class="msg ai">Conversación reiniciada. ¿En qué puedo ayudarte?</div>';
    }
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    response = assistant.chat(data["message"])
    return jsonify({"response": response})

@app.route("/reset", methods=["POST"])
def reset():
    assistant.reset()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)