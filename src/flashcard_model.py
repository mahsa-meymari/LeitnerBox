import pandas as pd
from datetime import date
import sqlite3

class FlashcardModel:
    def __init__(self): 
        self.conn = sqlite3.connect("leitnerbox.db")
        self.cursor = self.conn.cursor() 
        self.current_id = 0
        self._create_table_flashcards()

    def _create_table_flashcards(self):
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS flashcards (
  			   id INTEGER PRIMARY KEY AUTOINCREMENT,
         	    question TEXT NOT NULL,
                answer TEXT NOT NULL,
                example TEXT,
                box_number INTEGER NOT NULL,
                last_review_date TEXT,
                source Text
                )''')
        self.conn.commit()  # Save the changes

    def insert_flashcard(self, question, answer, example, box_number=1, last_reviewed_date=None,source=None):
        if not last_reviewed_date: last_reviewed_date=self._get_today_date()
        self.cursor.execute(
        '''INSERT INTO flashcards 
        (question, answer, example ,box_number, last_review_date, source) 
        VALUES (?, ?, ?, ?, ?,?)''', 
        (question, answer, example, box_number, last_reviewed_date,source))
        self.conn.commit()  # Save the changes
    
    def close_connection(self):
        self.conn.close()

    def delete_current_flashcard(self):    
        self.cursor.execute("DELETE FROM flashcards WHERE id = ?", (self.current_id,))
        self.conn.commit()
    
    def edit_flashcard(self, en, it, essempio):
        self.cursor.execute(
            "UPDATE flashcards SET question = ?, answer = ?, example = ?",
            (en,it,essempio))
    
    def move_card_to_next_box(self):
        new_box_no = min(5, self.get_flashcard_box()+1)
        # Update the box_number after a successful review
        self.cursor.execute(
            "UPDATE flashcards SET box_number = ?, last_review_date = ? WHERE id = ?",
            (new_box_no, self._get_today_date() , self.current_id)
        )
        self.conn.commit()

    def get_flashcard_question(self):
        self.cursor.execute("SELECT * FROM flashcards WHERE id = ?", (self.current_id,))
        flashcard = self.cursor.fetchall()[0]  # Get all matching rows
        return flashcard[1]
    
    
    def get_flashcard_answer(self):
        self.cursor.execute("SELECT * FROM flashcards WHERE id = ?", (self.current_id,))
        flashcard = self.cursor.fetchall()[0]  # Get all matching rows
        return flashcard[2]

    def get_flashcard_example(self):
        self.cursor.execute("SELECT * FROM flashcards WHERE id = ?", (self.current_id,))
        flashcard = self.cursor.fetchall()[0]  # Get all matching rows
        return flashcard[3]
    
    def get_flashcard_box(self):
        self.cursor.execute("SELECT * FROM flashcards WHERE id = ?", (self.current_id,))
        flashcard = self.cursor.fetchall()[0]  # Get all matching rows
        return flashcard[4]
    
    def get_flashcard_last_review_date(self):
        self.cursor.execute("SELECT * FROM flashcards WHERE id = ?", (self.current_id,))
        flashcard = self.cursor.fetchall()[0]  # Get all matching rows
        return flashcard[5]
    
    def get_flashcard_subject(self):
        self.cursor.execute("SELECT * FROM flashcards WHERE id = ?", (self.current_id,))
        flashcard = self.cursor.fetchall()[0]  # Get all matching rows
        return flashcard[6]
    
    @staticmethod
    def _get_today_date():
        return date.today().strftime("%Y-%m-%d")
    
    def return_card_to_first_box(self):
        # Update the box_number after a failed review
        self.cursor.execute(
            "UPDATE flashcards SET box_number = 1 , last_review_date = ? WHERE id = ?",
            (self._get_today_date() , self.current_id))
        self.conn.commit()

    def save_edited_flashcard(self, new_en, new_it, new_example):
        # Update the edited flashcard
        self.cursor.execute(
            '''UPDATE flashcards SET question = ?, answer = ?, example = ?
            WHERE id = ?''',
            (new_en, new_it, new_example, self.current_id))
        self.conn.commit()
    
    def get_count_cards_per_box(self):
        # Query to get the number of flashcards in each box
        self.cursor.execute('''
            SELECT box_number, COUNT(*) 
            FROM flashcards 
            GROUP BY box_number
        ''')
        box_counts = self.cursor.fetchall()

        result = {}
        # Print the number of flashcards in each box
        for box_number, count in box_counts:
            result[f"Box {box_number}"] = count
        for box_number in range(1,6):
            if box_number not in result.keys():
                result[box_number]=0
        return result
    
    def move_to_next_flashcard(self):
        # Query to get the total number of flashcards
        self.cursor.execute('SELECT COUNT(*) FROM flashcards')
        total_cards = self.cursor.fetchone()[0]
        self.current_id += 1
        if self.current_id >= total_cards:
            return False
        return True

    def load_excel_to_db(self, excel_path, source):
        # Load the Excel file into a pandas DataFrame
        df = pd.read_excel(excel_path)
        # Insert the data from the DataFrame into the database
        for row in df.itertuples(index=False, name=None):
            question = row[2]
            answer = row[1]
            box_number = row[3]
            if len(row)<5:
                self.insert_flashcard(question, answer, box_number, source=source)
            
            elif len(row)<6:
                self.insert_flashcard(question, answer, box_number, row[4], source=source)
            else: 
                last_reviewed_date = row[5]
                if pd.isna(last_reviewed_date):
                    last_reviewed_date = None
                elif not isinstance(last_reviewed_date, str): 
                    last_reviewed_date = last_reviewed_date.strftime("%Y-%m-%d")  
                self.insert_flashcard(question, answer, box_number, row[4], last_reviewed_date,source)
        print("Excel data loaded successfully into the database.")
