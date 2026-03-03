🤖 AI Assistant — Claude (Anthropic)
Asistente de texto conversacional en Python usando la API de Anthropic (Claude).
✨ Características
	∙	Conversación multi-turno con memoria del historial
	∙	Personalidad configurable vía config.py
	∙	Comandos integrados (/reset, /ayuda, /salir)
	∙	Manejo de errores y variables de entorno seguras
🚀 Instalación
# 1. Clona el repositorio
git clone https://github.com/tu-usuario/ai-assistant.git
cd ai-assistant

# 2. Crea un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Configura tu API key
cp .env.example .env
# Edita .env y agrega tu clave de Anthropic

🔑 Obtener API Key
	1.	Ve a console.anthropic.com
	2.	Crea una cuenta y genera una API key
	3.	Pégala en el archivo .env
