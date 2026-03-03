import os
from dotenv import load_dotenv
from assistant import AIAssistant

load_dotenv()

COMMANDS = {
    "/salir": "Terminar la sesión",
    "/reset": "Reiniciar la conversación",
    "/ayuda": "Mostrar esta ayuda",
}


def show_help():
    print("\n📋 Comandos disponibles:")
    for cmd, desc in COMMANDS.items():
        print(f"  {cmd:10} → {desc}")
    print()


def check_api_key():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: No se encontró ANTHROPIC_API_KEY.")
        print("   Crea un archivo .env con tu clave API.")
        print("   Ejemplo: ANTHROPIC_API_KEY=sk-ant-...")
        exit(1)


def main():
    check_api_key()

    print("=" * 50)
    print("🤖  Asistente IA con Claude (Anthropic)")
    print("=" * 50)
    print("Escribe tu mensaje o usa /ayuda para ver comandos.")
    print()

    assistant = AIAssistant()

    while True:
        try:
            user_input = input("Tú: ").strip()

            if not user_input:
                continue

            if user_input == "/salir":
                print("👋 ¡Hasta luego!")
                break
            elif user_input == "/reset":
                assistant.reset()
            elif user_input == "/ayuda":
                show_help()
            else:
                print("IA: ", end="", flush=True)
                response = assistant.chat(user_input)
                print(response)
                print()

        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    main()
