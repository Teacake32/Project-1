import os
import sqlite3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random

def create_database():
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS questions
                 (id INTEGER PRIMARY KEY, topic TEXT, question_path TEXT, answer_path TEXT)''')

    conn.commit()
    conn.close()


def insert_question(topic, question_path, answer_path):
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()

    c.execute("INSERT INTO questions (topic, question_path, answer_path) VALUES (?, ?, ?)", (topic, question_path, answer_path))

    conn.commit()
    conn.close()


def fetch_random_question(topic):
    conn = sqlite3.connect('questions.db')
    cur = conn.cursor()
    cur.execute("SELECT question_path, answer_path FROM questions WHERE topic=? ORDER BY RANDOM() LIMIT 1", (topic,))
    question = cur.fetchone()
    conn.commit()
    conn.close()
    return question


class ImageQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Quiz App")

        self.topic_var = tk.StringVar()
        self.topic_var.set("Select Topic")
        self.current_question = 1

        self.create_widgets()
        self.load_topics()

    def create_widgets(self):
        self.topic_label = ttk.Label(self.root, text="Select Topic:")
        self.topic_label.grid(row=0, column=0, padx=10, pady=5)

        self.topic_combobox = ttk.Combobox(self.root, textvariable=self.topic_var)
        self.topic_combobox.grid(row=0, column=1, padx=10, pady=5)
        self.topic_combobox.bind("<<ComboboxSelected>>", self.load_images)

        self.generate_button = ttk.Button(self.root, text="Generate Random Question", command=self.generate_random_question)
        self.generate_button.grid(row=0, column=2, padx=10, pady=5)

        self.answer_button = ttk.Button(self.root, text="Answer", command=self.show_answer)
        self.answer_button.grid(row=1, column=1, padx=10, pady=5)

        self.question_label = ttk.Label(self.root, text="Question:")
        self.question_label.grid(row=2, column=0, padx=10, pady=5)

        self.answer_label = ttk.Label(self.root, text="Answer:")
        self.answer_label.grid(row=2, column=1, padx=10, pady=5)

        self.question_image_label = ttk.Label(self.root)
        self.question_image_label.grid(row=3, column=0, padx=10, pady=5)

        self.answer_image_label = ttk.Label(self.root)

    def load_topics(self):
        topics = ['Topic 1', 'Topic 2', 'Topic 3', 'Topic 4', 'Topic 5', 'Topic 6', 'Topic 7']
        self.topic_combobox['values'] = topics

    def load_images(self, event=None):
        topic = self.topic_var.get()
        question_path, answer_path = fetch_random_question(topic)

        question_image = Image.open(os.path.join(os.path.dirname(__file__), question_path))
        question_image = question_image.resize((500, 500))
        question_photo = ImageTk.PhotoImage(question_image)

        self.question_image_label.config(image=question_photo)
        self.question_image_label.image = question_photo

        self.answer_image = Image.open(os.path.join(os.path.dirname(__file__), answer_path))
        self.answer_image = self.answer_image.resize((500, 500))

    def generate_random_question(self):
        topic = self.topic_var.get()
        self.load_images()

    def show_answer(self):
        answer_photo = ImageTk.PhotoImage(self.answer_image)

        self.answer_image_label.config(image=answer_photo)
        self.answer_image_label.image = answer_photo
        self.answer_image_label.grid(row=3, column=1, padx=10, pady=5)

def main():
    create_database()

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

if __name__ == "__main__":
    main()
