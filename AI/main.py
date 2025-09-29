from langchain.chat_models import init_chat_model

from Word_Assesment import Word_Assesment

CHAT_MODEL = "qwen3:0.6b"

class Main:
    def __init__(self):
        pass


    def play_game(self):
        """Main Game Loop"""

        print("Welcome to The Notebook")

        try:
            llm = init_chat_model(CHAT_MODEL, model_provider='ollama')
        except Exception as e:
            print(f"Error connecting LLM: {e}")
            print(f"Rerun Ollama - {CHAT_MODEL}")

            return

        while True:
            print("\nOptions:")
            print("1. Start a new game\n"
                  "2. Quit")

            choice = input("Enter your choice: ").strip()

            if choice == "2":
                print("Ok. Bye")
                break
            elif choice == "1":
                try:
                    Word_Assesment(llm).start_new_game(llm, theme = "")
                except Exception as e:
                    print(f"Error when starting game: {e}")
            else:
                print("\n Nuh UH.")


if __name__ == "__main__":
    Main().play_game()
