import sys
from src.flashcard_UI import FlashcardUI
from src.flashcard_model import FlashcardModel
from src.flashcard_controller import FlashcardController


def main():
    fc_model = FlashcardModel()
    fc_ui = FlashcardUI()
    controller = FlashcardController(fc_model, fc_ui)
    
    controller.start()

if __name__ == "__main__":
    main()