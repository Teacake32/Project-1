import os
import sqlite3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


def create_database():#creating the databse simple SQL statement
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS questions
                 (id INTEGER PRIMARY KEY, topic TEXT, question_path TEXT, answer_path TEXT)''') #database is called questions but each table is sorted by topic

    conn.commit()
    conn.close()


def insert_question(topic, question_path, answer_path): # using the iteration of the files to insert into the question numbers and the topics ect
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()

    c.execute("INSERT INTO questions (topic, question_path, answer_path) VALUES (?, ?, ?)", (topic, question_path, answer_path))

    conn.commit()
    conn.close()


def fetch_questions(topic): # this function allows the  tkinter module to gain access to each topic from the sql query and database, it is gathering the file pathways based of the topic number
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()

    c.execute("SELECT question_path, answer_path FROM questions WHERE topic=?", (topic,))
    questions = c.fetchall()

    conn.close()

    return questions

def fetch_questions_random (topic): 
  conn = sqlite3.connect('questions.db')
  cur = conn.cursor()
  cur.execute("SELECT question_path, answer_path FROM questions WHERE topic=? AND ORDER BY RANDOM() LIMIT 1" )
  questions = cur.fetchall()
  conn.commit()
  conn.close()
  return questions 
  

class ImageQuizApp: #this class while looks confusing is just a bunch of fetch statments and configuration for each size of quesiton box
    def __init__(self, root):
        self.root = root
        self.root.title("Image Quiz App")

        self.topic_var = tk.StringVar()
        self.topic_var.set("Select Topic")
        self.current_question = 1  #counter to show what question number we are on so we can move between questions

        self.create_widgets()
        self.load_topics()

    def create_widgets(self): # not fully undersood mainly video copy
        self.topic_label = ttk.Label(self.root, text="Select Topic:")
        self.topic_label.grid(row=0, column=0, padx=10, pady=5)

        self.topic_combobox = ttk.Combobox(self.root, textvariable=self.topic_var)
        self.topic_combobox.grid(row=0, column=1, padx=10, pady=5)
        self.topic_combobox.bind("<<ComboboxSelected>>", self.load_images)

        self.prev_button = ttk.Button(self.root, text="Previous", command=self.show_previous_question)
        self.prev_button.grid(row=1, column=0, padx=10, pady=5)

        self.next_button = ttk.Button(self.root, text="Next", command=self.show_next_question)
        self.next_button.grid(row=1, column=1, padx=10, pady=5)

        self.question_label = ttk.Label(self.root, text="Question:")
        self.question_label.grid(row=2, column=0, padx=10, pady=5)

        self.answer_label = ttk.Label(self.root, text="Answer:")
        self.answer_label.grid(row=2, column=1, padx=10, pady=5)

        self.question_image_label = ttk.Label(self.root) #image for the question designated box - sushi is a fluffy cat
        self.question_image_label.grid(row=3, column=0, padx=10, pady=5)

        self.answer_image_label = ttk.Label(self.root) #image for the answer designated box - elmo is a fluffy cat
        self.answer_image_label.grid(row=3, column=1, padx=10, pady=5)

    def load_topics(self):
        topics = ['Topic 1', 'Topic 2', 'Topic 3', 'Topic 4', 'Topic 5', 'Topic 6', 'Topic 7']
        self.topic_combobox['values'] = topics #this is creating a box at the top  that allows the user to select between boxes

    def load_images(self, event=None): #inserting the images into designated boxes
        topic = self.topic_var.get()

        #creating the file pathways on Haris' naming convention (minus 1 is needed it is using an iterated loop data)
        question_path = f"t{topic[-1]}question{self.current_question}.png"
        answer_path = f"t{topic[-1]}answer{self.current_question}.png"

        #this part is just constructing a full path using all the // and drive naviation
        question_image = Image.open(os.path.join(os.path.dirname(__file__), question_path)) #question
        question_image = question_image.resize((500, 500))
        question_photo = ImageTk.PhotoImage(question_image)

        self.question_image_label.config(image=question_photo)
        self.question_image_label.image = question_photo

        answer_image = Image.open(os.path.join(os.path.dirname(__file__), answer_path)) #answer
        answer_image = answer_image.resize((500, 500))
        answer_photo = ImageTk.PhotoImage(answer_image)

        self.answer_image_label.config(image=answer_photo)
        self.answer_image_label.image = answer_photo

    def show_previous_question(self): # button that lets you navigate
        if self.current_question > 1:
            self.current_question -= 1
            self.load_images()

    def show_next_question(self): #button that lets you navigate
        if self.current_question < 5: #must be changed if there is more than 5 questions ever
            self.current_question += 1
            self.load_images()

def main(): # iterating through all the sample data
    create_database()
    #story time - when i first made this it was all inserted manually and said i would steal elmo if jed tried to make it iterable through a loop
    # Insert sample data
    for topic in range(1, 8):
        for i in range(1, 6):
            topic_name = f"Topic {topic}"
            question_path = f"t{topic}question{i}.png"
            answer_path = f"t{topic}answer{i}.png"
            insert_question(topic_name, question_path, answer_path)

    root = tk.Tk()
    app = ImageQuizApp(root)
    root.mainloop()

if __name__ == "__main__": #  the video told me to do this i have not idea how it interacts with the class controlling tkinter
    main()
