import pandas as pd
from datetime import date

class FlashcardModel:
    def __init__(self, file_path):
        self.file_path = file_path
        self.current_index = 0
        self._load_data()

    def _load_data(self):
        self.df = pd.read_excel(self.file_path)
        if not 'En' in self.df.columns or not 'It' in self.df.columns or not 'Essempio' in self.df.columns:
            raise ValueError('This file does not have "En" or "It" or "Essempio" column')
        self.df['Essempio'] = self.df['Essempio'].fillna("")
        # Check if the 'Box' column exists If it doesn't exist, create it with a default value of 1
        if 'Box' not in self.df.columns:
            self.df['Box'] = 1
        else:
            # If it exists, replace None values with 1
            self.df['Box'] = self.df['Box'].fillna(1)
        # Check if the 'LRD' column exists
        if 'LRD' not in self.df.columns:
            self.df['LRD'] = None
        self.df["LRD"] = pd.to_datetime(self.df["LRD"], errors="coerce").dt.date
        self.df = self.df.dropna(subset=['En', 'It'], how='all')

        # Replace all '/' with '-'
        self.df = self.df.replace('/', '-', regex=True)
        self.save()
        return True
    
    def modify_flashcard(self, en, it, essempio):
        self.df.at[self.current_index, 'En'] = en
        self.df.at[self.current_index, 'It'] = it
        self.df.at[self.current_index, 'Essempio'] = essempio

    def get_flashcard(self):
        # Return the current flashcard details (e.g., English, Italian, Example)
        return self.df.loc[self.current_index, ['En', 'It', 'Essempio', 'Box']]

    def move_to_next_flashcard(self):
        self.current_index += 1
        if self.current_index >= len(self.df) or pd.isna(self.df.at[self.current_index, 'En']):
            return False
        return True
        
    def delete_current_flashcard(self):
        self.df = self.df.drop(index=self.current_index)
        self.save()


    def move_card_to_next_box(self):
        new_box_no = min(5, self.df.at[self.current_index, 'Box']+1)
        self.df.at[self.current_index, 'Box'] = new_box_no
        self.df.at[self.current_index, 'LRD'] = date.today()
        self.save()

    def return_cart_to_first_box(self):
        self.df.at[self.current_index, 'Box'] = 1
        self.save()

    def get_card_box_LRD(self):
        return self.df.loc[self.current_index, ['Box', 'LRD']]
    
    def save_edited_flashcard(self, new_en, new_it, new_example):
        self.df.at[self.current_index, 'En'] = new_en
        self.df.at[self.current_index, 'It'] = new_it
        self.df.at[self.current_index, 'Essempio'] = new_example
        self.save()
        
    
    def get_numof_cards_in_box(self,box_no):
        return len(self.df[self.df['Box'] == box_no])

    
    def save(self):
        self.df.to_excel(self.file_path, index=False)