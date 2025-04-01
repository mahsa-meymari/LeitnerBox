from datetime import date, timedelta
from gtts import gTTS
import os
import subprocess

class FlashcardController:
    def __init__(self,fc_model,fc_ui):
        self.fc_model = fc_model
        self.fc_ui = fc_ui
        self.wrong_no = 0
        self.correct_no = 0
        
        self.fc_ui.back_button.config(command=self.rotate_flashcard)
        self.fc_ui.correct_button.config(command=self.is_correct)
        self.fc_ui.wrong_button.config(command=self.is_wrong)
        self.fc_ui.edit_button.config(command=self.edit_flashcard)
        self.fc_ui.save_button.config(command=self.save_edited_flashcard)
        self.fc_ui.cancel_button.config(command=self.show_flashcard)
        self.fc_ui.start_button.config(command=self.show_flashcard)
        self.fc_ui.delete_button.config(command=self.delete_flashcard)
        self.fc_ui.play_example_button.config(command=self.play_example)
        self.fc_ui.play_it_button.config(command=self.play_it)

        self.fc_ui.root.bind("<Return>", lambda event: self.rotate_flashcard() if self.fc_ui.get_current_frame() == self.fc_ui.front_frame else None)
        self.fc_ui.root.bind("<Right>", lambda event: self.is_correct() if self.fc_ui.get_current_frame() == self.fc_ui.back_frame else None)
        self.fc_ui.root.bind("<Left>", lambda event: self.is_wrong() if self.fc_ui.get_current_frame() == self.fc_ui.back_frame  else None)
        self.next_card()
    
    def edit_flashcard(self):
        en = self.fc_model.get_flashcard_question()
        it = self.fc_model.get_flashcard_answer()
        example = self.fc_model.get_flashcard_example()
        self.fc_ui.show_edit_flashcard(en, it, example)

    def _should_show_flashcard(self):
        """
        Logic to check if the current flashcard should be displayed based on its 'Box' and 'LRD' values.
        """
        box = self.fc_model.get_flashcard_box()
        LRD = self.fc_model.get_flashcard_last_review_date()
        LRD_date = date.fromisoformat(LRD)
        return (
             box == 1 or
            (box == 2 and LRD_date <= (date.today() - timedelta(days=2))) or
            (box == 3 and LRD_date <= (date.today() - timedelta(days=5))) or
            (box == 4 and LRD_date <= (date.today() - timedelta(days=10))) or
            (box == 5 and LRD_date <= (date.today() - timedelta(days=30)))
        )
    
    def rotate_flashcard(self):
        en = self.fc_model.get_flashcard_question()
        it = self.fc_model.get_flashcard_answer()
        example = self.fc_model.get_flashcard_example()
        your_answer_color = 'green' if self.fc_ui.get_answer().lower() == it.lower() else 'red'
        self.fc_ui.show_flashcard_back(en, it, example, your_answer_color)
        self.fc_ui.root.after(100, self.read_italian, it)  # 100 ms delay (can be adjusted)

    def next_card(self):
        unfinished = self.fc_model.move_to_next_flashcard()
        if not unfinished:
            self.fc_ui.show_end_page()
            return
        
        while not self._should_show_flashcard():
            unfinished = self.fc_model.move_to_next_flashcard()
            if not unfinished:
                self.fc_ui.show_end_page()
                return
        self.show_flashcard()

    def is_correct(self):
        """Handle correct answer: move the card to the next box."""
        self.fc_model.move_card_to_next_box()
        self.correct_no+=1
        self.next_card()

    def is_wrong(self):
        """Handle wrong answer: move the card to the first box."""
        self.fc_model.return_card_to_first_box()
        self.wrong_no+=1
        self.next_card()

    def save_edited_flashcard(self):
        # Retrieve values from entry fields
        new_en = self.fc_ui.en_entry.get()
        new_it = self.fc_ui.it_entry.get()
        new_example = self.fc_ui.eg_entry.get()
        self.fc_model.save_edited_flashcard(new_en, new_it, new_example)
        self.show_flashcard()

    def show_flashcard(self):
        en = self.fc_model.get_flashcard_question()
        box_no = self.fc_model.get_flashcard_box()
        subject = self.fc_model.get_flashcard_subject()
        self.fc_ui.show_flashcard_front(en, self.wrong_no, self.correct_no, box_no, subject)

    def show_first_page(self):
        count_per_boxs = self.fc_model.get_count_cards_per_box()
        no_cards_for_today = self.fc_model.get_no_cards_for_today()
        self.fc_ui.show_first_page(list(count_per_boxs.values()),no_cards_for_today)
        

    def start(self):
        self.show_first_page()
        self.fc_ui.start_UI()

    def delete_flashcard(self):
        self.fc_model.delete_current_flashcard()
        self.next_card()

    def play_example(self):
        example= self.fc_model.get_flashcard_example()
        self.read_italian(example)
    
    def play_it(self):
        it= self.fc_model.get_flashcard_answer()
        self.read_italian(it)

    def read_italian(self,text):
        file_path = f"data/voices/{text}.mp3"

        # Check if the file already exists
        if not os.path.exists(file_path):
            # Set language to Italian and create the speech
            tts = gTTS(text=text, lang='it', slow=False)
            # Save the audio file
            tts.save(file_path)
        
        # Play the sound
        subprocess.run(["afplay", file_path])