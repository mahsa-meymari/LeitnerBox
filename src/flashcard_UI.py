import tkinter as tk

class FlashcardUI:

    def __init__(self, fontsize=30, fontfamily="Arial"):
        # Create UI window
        self.fontsize = fontsize
        self.fontfamily = fontfamily
        self.root = tk.Tk()
        self.root.title("Flash Cards")
        self.root.geometry("1000x600")

        # Create frames for each page
        self.front_frame = tk.Frame(self.root)
        self.back_frame = tk.Frame(self.root)
        self.edit_frame = tk.Frame(self.root)
        self.first_frame = tk.Frame(self.root)
        self.end_frame = tk.Frame(self.root)

        for frame in (self.front_frame, self.back_frame, self.edit_frame, self.first_frame, self.end_frame):
            frame.grid(row=0, column=0, columnspan=5 ,sticky="nsew")

        
        # Create and center widgets
        self.counter_label = tk.Label(self.root, font=(self.fontfamily, self.fontsize))
        self.counter_label.grid(row=0, column=10, columnspan=5, sticky="nw")


        # Configure grid weights to make sure the content is centered
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Build pages
        self.build_first_page()
        self.build_front_page()
        self.build_back_page()
        self.build_edit_page()
        self.build_end_page()

        # Keep track of current frame
        self._current_frame = None
 
    def build_first_page(self):
            # Configure row and column weights for front frame to center widgets
            self.first_frame.grid_rowconfigure(0, weight=1)
            self.first_frame.grid_rowconfigure(1, weight=1)
            self.first_frame.grid_rowconfigure(5, weight=1)
            self.first_frame.grid_columnconfigure(0, weight=1)
            self.first_frame.grid_columnconfigure(1, weight=1)

            self.file_name_label = tk.Label(self.first_frame, font=(self.fontfamily, self.fontsize))
            self.no_cards_label = tk.Label(self.first_frame, font=(self.fontfamily, self.fontsize))
            self.box_labels = [tk.Label(self.first_frame, font=(self.fontfamily, self.fontsize)) for _ in range(5)]
            
            self.start_button = tk.Button(self.first_frame, text="Start", font=("Arial", self.fontsize))

            
            self.file_name_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")
            
            for i in range(5):
                self.box_labels[i].grid(row=i+1, column=0, columnspan=2, pady=10, sticky="nsew")
            
            self.start_button.grid(row=6, column=0, columnspan=2, pady=10, sticky="nsew")
    
    def build_end_page(self):
        self.end_frame.grid_rowconfigure(0, weight=1)
        self.end_frame.grid_columnconfigure(0, weight=1)
        self.end_label = tk.Label(self.end_frame, text='The end', font=(self.fontfamily, self.fontsize))
        self.end_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")
    
    def build_front_page(self):
        # Configure row and column weights for front frame to center widgets
        self.front_frame.grid_rowconfigure(0, weight=1)
        self.front_frame.grid_rowconfigure(1, weight=1)
        self.front_frame.grid_columnconfigure(0, weight=1)
        self.front_frame.grid_columnconfigure(1, weight=1)

        self.en_label_front = tk.Label(self.front_frame, font=(self.fontfamily, self.fontsize))
        self.answer = tk.Entry(self.front_frame, width=30, font=(self.fontfamily, self.fontsize))
        self.back_button = tk.Button(self.front_frame, text="Back", font=("Arial", self.fontsize))
        self.box_no_label = tk.Label(self.front_frame, font=(self.fontfamily, self.fontsize), text='boxno', foreground='yellow')

        self.box_no_label.grid(row=0, column=3, columnspan=1, pady=10,sticky="nsew" )
        self.en_label_front.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")
        self.answer.grid(row=1, column=0, columnspan=5, pady=10, sticky="nsew")
        self.back_button.grid(row=2, column=0, columnspan=5, pady=10, sticky="nsew")

    def build_back_page(self):
        self.back_frame.grid_rowconfigure(0, weight=1)
        self.back_frame.grid_rowconfigure(1, weight=1)
        self.back_frame.grid_rowconfigure(2, weight=1)
        self.back_frame.grid_rowconfigure(3, weight=1)
        self.back_frame.grid_rowconfigure(4, weight=1)
        self.back_frame.grid_rowconfigure(5, weight=1)
        self.back_frame.grid_rowconfigure(6, weight=1)
        self.back_frame.grid_columnconfigure(0, weight=1)
        self.back_frame.grid_columnconfigure(1, weight=1)

        self.en_label_back = tk.Label(self.back_frame, font=("Arial", self.fontsize))
        self.it_label = tk.Label(self.back_frame, font=("Arial", self.fontsize))
        self.eg_label = tk.Label(self.back_frame, font=("Arial", self.fontsize // 2))
        self.your_answer_label = tk.Label(self.back_frame, font=("Arial", self.fontsize))
        self.correct_button = tk.Button(self.back_frame, text="Correct", font=("Arial", self.fontsize), foreground='green',padx=10, pady=10)
        self.wrong_button = tk.Button(self.back_frame, text="Wrong", font=("Arial", self.fontsize), foreground='red',padx=10, pady=10)
        self.edit_button = tk.Button(self.back_frame, text="Edit", font=("Arial", self.fontsize),padx=10, pady=10)
        self.delete_button = tk.Button(self.back_frame, text="Delete", font=("Arial", self.fontsize),padx=10, pady=10)
        self.play_example_button = tk.Button(self.back_frame, text="🔊", font=("Arial", 25),padx=2, pady=2, background='Black')
        self.play_it_button = tk.Button(self.back_frame, text="🔊", font=("Arial", 25),padx=2, pady=2, background='black')

        self.en_label_back.grid(row=0, column=0, columnspan=5, pady=10, sticky="nsew")
        self.your_answer_label.grid(row=1, column=0, columnspan=5, pady=10, sticky="nsew")
        self.it_label.grid(row=2, column=0, columnspan=5, pady=10, sticky="nsew")
        self.eg_label.grid(row=3, column=0, columnspan=4, pady=10, sticky="nsew")
        
        self.wrong_button.grid(row=4, column=0, columnspan=2, sticky="sw")
        self.correct_button.grid(row=4, column=3, columnspan=2, sticky="se")
        self.edit_button.grid(row=6, column=0, columnspan=2, pady=10, sticky="sw")
        self.delete_button.grid(row=6, column=3, columnspan=2, pady=10, sticky="sw")
        self.play_example_button.grid(row=3, column=4, columnspan=1, sticky="nsew")
        self.play_it_button.grid(row=2,column=4, columnspan=1, sticky="nsew")

    def build_edit_page(self):
        self.edit_frame.grid_rowconfigure(0, weight=1)
        self.edit_frame.grid_rowconfigure(1, weight=1)
        self.edit_frame.grid_rowconfigure(2, weight=1)
        self.edit_frame.grid_rowconfigure(3, weight=1)
        self.edit_frame.grid_rowconfigure(4, weight=1)
        self.edit_frame.grid_columnconfigure(0, weight=1)
        self.edit_frame.grid_columnconfigure(1, weight=1)

        self.en_label_edit = tk.Label(self.edit_frame, text="English:", font=("Arial", self.fontsize))
        self.it_label_edit = tk.Label(self.edit_frame, text="Italian:", font=("Arial", self.fontsize))
        self.eg_label_edit = tk.Label(self.edit_frame, text="Example:", font=("Arial", self.fontsize // 2))
        
        self.en_entry = tk.Entry(self.edit_frame, font=("Arial", self.fontsize))
        self.it_entry  = tk.Entry(self.edit_frame, font=("Arial", self.fontsize))
        self.eg_entry = tk.Entry(self.edit_frame, font=("Arial", self.fontsize // 2))

        self.save_button = tk.Button(self.edit_frame, text="Save", font=("Arial", self.fontsize))
        self.cancel_button = tk.Button(self.edit_frame, text="Cancel", font=("Arial", self.fontsize))


        self.en_label_edit.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")
        self.it_label_edit.grid(row=1, column=0, columnspan=3, pady=10, sticky="nsew")
        self.eg_label_edit.grid(row=2, column=0, columnspan=3, pady=10, sticky="nsew")

        self.en_entry.grid(row=0, column=1, columnspan=3, pady=10, sticky="nsew")
        self.it_entry.grid(row=1, column=1, columnspan=3, pady=10, sticky="nsew")
        self.eg_entry.grid(row=2, column=1, columnspan=3, pady=10, sticky="nsew")

        self.save_button.grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.cancel_button.grid(row=4, column=0, columnspan=2, sticky="nsew")

    def show_flashcard_front(self, en, wrong_no, correct_no, box_no):
        self.en_label_front.config(text=en)
        self.box_no_label.config(text=f'BOX {box_no}')
        self.answer.delete(0, tk.END)
        self.counter_label.config(text=f"Correct: {correct_no} \nWrong: {wrong_no}")
        self.front_frame.tkraise()
        self._current_frame = self.front_frame

    def show_flashcard_back(self, en, it, example, your_answer_color):
        self.back_frame.tkraise()
        self.en_label_back.config(text=en)  # Show English text
        self.it_label.config(text=it)  # Show Italian text
        self.eg_label.config(text=example)  # Show Italian example
        self.your_answer_label.config(text=self.get_answer(), fg=your_answer_color)
        self._current_frame = self.back_frame

    def show_edit_flashcard(self, en, it, example):
        self.edit_frame.tkraise()
        self.en_entry.delete(0, tk.END)
        self.it_entry.delete(0, tk.END)
        self.eg_entry.delete(0, tk.END)
        self.en_entry.insert(0, en)
        self.it_entry.insert(0, it)
        self.eg_entry.insert(0, example)
        self._current_frame = self.edit_frame
    
    def show_first_page(self, file_name, boxes):
         self.first_frame.tkraise()
         print(f"first {file_name}")
         self.file_name_label.config(text=f"File: {file_name}")
         for i in range(5):
             self.box_labels[i].config(text=f"box {i+1}: {boxes[i]}")
         self._current_frame = self.first_frame
         

    def show_end_page(self):
        self.end_frame.tkraise()
        self._current_frame = self.end_frame

    def get_answer(self):
        return self.answer.get()
    
    def start_UI(self):
        # Start the UI loop
        self.root.mainloop()

    def get_current_frame(self):
        return self._current_frame