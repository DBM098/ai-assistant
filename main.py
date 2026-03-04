from dotenv import load_dotenv
load_dotenv()

from assistant import AIAssistant


def main():
    print("=== Asistente de IA ===")
    print("Escribe 'salir' para terminar o 'reset' para reiniciar la conversación.\n")

    assistant = AIAssistant()

    while True:
        try:
            user_input = input("Tú: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ("salir", "exit", "quit"):
                print("¡Hasta luego!")
                break

            if user_input.lower() == "reset":
                assistant.reset()
                continue

            response = assistant.chat(user_input)
            print(f"\nAsistente: {response}\n")

        except KeyboardInterrupt:
            print("\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
