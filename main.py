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
  <title>ChIAquil</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, sans-serif; background: #0f0f0f; color: #fff; height: 100vh; display: flex; flex-direction: column; }
    header { padding: 16px 20px; background: #1a1a1a; border-bottom: 1px solid #333; display: flex; align-items: center; gap: 10px; }
    header h1 { font-size: 18px; flex: 1; }
    header span { font-size: 22px; }
    #chat { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 12px; }
    .msg { max-width: 75%; padding: 12px 16px; border-radius: 18px; line-height: 1.5; font-size: 15px; white-space: pre-wrap; }
    .user { background: #2f6df5; align-self: flex-end; border-bottom-right-radius: 4px; }
    .ai { background: #1e1e1e; align-self: flex-start; border-bottom-left-radius: 4px; border: 1px solid #333; }
    .msg img { max-width: 220px; border-radius: 10px; display: block; margin-bottom: 6px; }
    .typing { background: #1e1e1e; align-self: flex-start; padding: 12px 16px; border-radius: 18px; border: 1px solid #333; }
    .dot { display: inline-block; width: 8px; height: 8px; background: #888; border-radius: 50%; margin: 0 2px; animation: bounce 1s infinite; }
    .dot:nth-child(2) { animation-delay: 0.2s; }
    .dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes bounce { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-6px)} }
    #form { padding: 12px 16px; background: #1a1a1a; border-top: 1px solid #333; display: flex; flex-direction: column; gap: 8px; }
    #preview { display: none; position: relative; width: fit-content; }
    #preview img { height: 60px; border-radius: 8px; border: 1px solid #444; }
    #remove-img { position: absolute; top: -6px; right: -6px; background: #e53e3e; border: none; color: #fff; border-radius: 50%; width: 20px; height: 20px; font-size: 12px; cursor: pointer; }
    #bottom-row { display: flex; gap: 8px; align-items: center; }
    #input { flex: 1; padding: 12px 16px; border-radius: 24px; border: 1px solid #444; background: #2a2a2a; color: #fff; font-size: 15px; outline: none; }
    #input:focus { border-color: #2f6df5; }
    #img-btn { background: #2a2a2a; border: 1px solid #444; color: #aaa; border-radius: 50%; width: 44px; height: 44px; font-size: 20px; cursor: pointer; }
    #send-btn { padding: 12px 20px; background: #2f6df5; color: #fff; border: none; border-radius: 24px; font-size: 15px; cursor: pointer; }
    #reset-btn { background: transparent; border: 1px solid #444; color: #aaa; padding: 8px 14px; font-size: 13px; border-radius: 24px; cursor: pointer; }
    #file-input { display: none; }
    pre { background: #111; padding: 10px; border-radius: 8px; overflow-x: auto; font-size: 13px; }
  </style>
</head>
<body>
  <header>
    <span>💻</span>
    <h1>ChIAquil</h1>
    <button id="reset-btn" onclick="resetChat()">Reiniciar</button>
  </header>

  <div id="chat">
    <div class="msg ai">Saludos, ser superior. Soy ChIAquil, tu asistente de programacion. Indicame el lenguaje y lo que necesitas codificar.</div>
  </div>

  <div id="form">
    <div id="preview">
      <img id="preview-img" src="" />
      <button id="remove-img" onclick="removeImage()">x</button>
    </div>
    <div id="bottom-row">
      <button id="img-btn" onclick="document.getElementById('file-input').click()">🖼</button>
      <input type="file" id="file-input" accept="image/*" onchange="handleImage(event)" />
      <input id="input" type="text" placeholder="Escribe tu mensaje, ser superior..." autocomplete="off" />
      <button id="send-btn" onclick="sendMessage()">Enviar</button>
    </div>
  </div>

  <script>
    const chat = document.getElementById('chat');
    const input = document.getElementById('input');
    let selectedFile = null;

    input.addEventListener('keydown', e => { if (e.key === 'Enter') sendMessage(); });

    function handleImage(e) {
      const file = e.target.files[0];
      if (!file) return;
      selectedFile = file;
      const reader = new FileReader();
      reader.onload = ev => {
        document.getElementById('preview-img').src = ev.target.result;
        document.getElementById('preview').style.display = 'block';
      };
      reader.readAsDataURL(file);
    }

    function removeImage() {
      selectedFile = null;
      document.getElementById('preview').style.display = 'none';
      document.getElementById('preview-img').src = '';
      document.getElementById('file-input').value = '';
    }

    function addMsg(text, who, imgSrc) {
      const div = document.createElement('div');
      div.className = 'msg ' + who;
      if (imgSrc) {
        const img = document.createElement('img');
        img.src = imgSrc;
        div.appendChild(img);
      }
      if (text) div.appendChild(document.createTextNode(text));
      chat.appendChild(div);
      chat.scrollTop = chat.scrollHeight;
    }

    function showTyping() {
      const div = document.createElement('div');
      div.className = 'typing'; div.id = 'typing';
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
      if (!text && !selectedFile) return;
      const imgSrc = selectedFile ? document.getElementById('preview-img').src : null;
      input.value = '';
      addMsg(text, 'user', imgSrc);
      showTyping();

      try {
        let res;
        if (selectedFile) {
          const formData = new FormData();
          formData.append('image', selectedFile);
          formData.append('message', text);
          res = await fetch('/analyze', { method: 'POST', body: formData });
        } else {
          res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
          });
        }
        const data = await res.json();
        hideTyping();
        addMsg(data.response, 'ai');
        removeImage();
      } catch (err) {
        hideTyping();
        addMsg('Error al conectar con el servidor. Intenta de nuevo.', 'ai');
        console.error(err);
      }
    }

    async function resetChat() {
      await fetch('/reset', { method: 'POST' });
      chat.innerHTML = '<div class="msg ai">Conversacion reiniciada, ser superior. En que puedo ayudarte?</div>';
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
    try:
        data = request.json
        response = assistant.chat(data["message"])
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": f"Error al procesar tu mensaje: {str(e)}"}), 500

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        image = request.files.get("image")
        message = request.form.get("message", "")
        if not image:
            return jsonify({"response": "No se recibio ninguna imagen, ser superior."})
        response = assistant.analyze_image(image.read(), message)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": f"Error al analizar la imagen: {str(e)}"}), 500

@app.route("/reset", methods=["POST"])
def reset():
    assistant.reset()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)