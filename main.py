import sys
from src.flashcard_UI import FlashcardUI
from src.flashcard_model import FlashcardModel
from src.flashcard_controller import FlashcardController


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <filename>")
        sys.exit(1)
    
    file_name = sys.argv[1]  # Get the file name from command-line argument
    file_path = f"data/{file_name}.xlsx"  # Construct the path
    
    fc_model = FlashcardModel(file_path)
    fc_ui = FlashcardUI()
    controller = FlashcardController(fc_model, fc_ui)
    
    controller.start(file_name)
    fc_model.save()

if __name__ == "__main__":
    main()