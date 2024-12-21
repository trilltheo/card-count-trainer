import tkinter as tk
from PIL import Image, ImageTk
import random
import time
import os
import sys

def resource_path(relative_path):
    """Получает путь к ресурсу в зависимости от того, запущен ли скрипт из .exe или нет."""
    if hasattr(sys, '_MEIPASS'):
        # Если приложение запущено из PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        # Если приложение запущено как скрипт
        return os.path.join(os.path.abspath("."), relative_path)

CARD_VALUES = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

CARDS = list(CARD_VALUES.keys())
SUITS = ['hearts', 'diamonds', 'clubs', 'spades']

class CardCountingTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Counting Trainer")
        self.root.geometry("1000x600")  # Размер окна

        self.current_card = None
        self.card_number = 0
        self.running_count = 0
        self.auto_playing = False

        self.deck_count = 1
        self.deck = []
        self.generate_deck()

        self.start_time = None
        self.card_times = []

        self.card_image_label = tk.Label(root, bg="#f5f5f5")
        self.card_image_label.place(x=125, y=20)

        self.card_number_label = tk.Label(root, text="Card Number: 0", font=("Helvetica", 16), bg="#f5f5f5")
        self.card_number_label.place(x=125, y=230)

        self.new_card_button = tk.Button(root, text="Show New Card", command=self.show_new_card, font=("Helvetica", 14), bg="#4CAF50", fg="white", relief="raised", bd=5)
        self.new_card_button.place(x=125, y=270)

        self.entry = tk.Entry(root, font=("Helvetica", 16))
        self.entry.place(x=85, y=330)

        self.check_button = tk.Button(root, text="Check Count", command=self.check_count, font=("Helvetica", 14), bg="#2196F3", fg="white", relief="raised", bd=5)
        self.check_button.place(x=30, y=370)

        self.result_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#f5f5f5")
        self.result_label.place(x=100, y=420)

        self.stats_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#f5f5f5")
        self.stats_label.place(x=600, y=270)

        self.auto_play_button = tk.Button(root, text="Start Auto-Play", command=self.toggle_auto_play, font=("Helvetica", 14), bg="#FF9800", fg="white", relief="raised", bd=5)
        self.auto_play_button.place(x=750, y=90)

        self.speed_label = tk.Label(root, text="Speed (ms):", font=("Helvetica", 12), bg="#f5f5f5")
        self.speed_label.place(x=450, y=100)

        self.speed_entry = tk.Entry(root, font=("Helvetica", 12))
        self.speed_entry.insert(0, "1000")
        self.speed_entry.place(x=550, y=100)

        self.deck_label = tk.Label(root, text="Decks (1-8):", font=("Helvetica", 12), bg="#f5f5f5")
        self.deck_label.place(x=450, y=150)

        self.deck_entry = tk.Entry(root, font=("Helvetica", 12))
        self.deck_entry.insert(0, "1")
        self.deck_entry.place(x=550, y=150)

        self.set_deck_button = tk.Button(root, text="Set Deck Count", command=self.set_deck_count, font=("Helvetica", 12), bg="#FF5722", fg="white", relief="raised", bd=5)
        self.set_deck_button.place(x=750, y=140)

        self.restart_button = tk.Button(root, text="Restart", command=self.restart, font=("Helvetica", 12), bg="#9C27B0", fg="white", relief="raised", bd=5)
        self.restart_button.place(x=450, y=330)


        self.stats_button = tk.Button(root, text="Show Stats", command=self.show_stats, font=("Helvetica", 14), bg="#2196F3", fg="white", relief="raised", bd=5)
        self.stats_button.place(x=450, y=270)


        self.show_answers_button = tk.Button(root, text="Show Answer Options", command=self.show_answer_options, font=("Helvetica", 14), bg="#673AB7", fg="white", relief="raised", bd=5)
        self.show_answers_button.place(x=200, y=370)

        self.answer_buttons = []

        self.display_face_down_card()

    def generate_deck(self):

        self.deck = [f"{card}_of_{suit}" for card in CARDS for suit in SUITS] * self.deck_count
        random.shuffle(self.deck)

    def set_deck_count(self):

        try:
            count = int(self.deck_entry.get())
            if 1 <= count <= 8:
                self.deck_count = count
                self.generate_deck()
                self.restart()
            else:
                self.result_label.config(text="Please enter a number between 1 and 8.", fg="red")
        except ValueError:
            self.result_label.config(text="Please enter a valid number.", fg="red")

    def show_new_card(self):

        if not self.deck:
            self.result_label.config(text="Deck is empty! Restart or add more decks.", fg="red")
            return

        if self.start_time is None:
            self.start_time = time.time()

        if self.card_number > 0:
            self.card_times.append(time.time() - self.start_time)

        self.start_time = time.time()

        card = self.deck.pop()
        self.card_number += 1

        card_value = card.split("_of_")[0]
        self.running_count += CARD_VALUES.get(card_value, 0)


        try:
            card_image = Image.open(resource_path(f"cards/{card}.png"))
            card_image = card_image.resize((150, 200))
            card_photo = ImageTk.PhotoImage(card_image)
            self.card_image_label.config(image=card_photo)
            self.card_image_label.image = card_photo
        except FileNotFoundError:
            self.card_image_label.config(text="Image not found", font=("Helvetica", 16))

        self.result_label.config(text="")
        self.card_number_label.config(text=f"Card Number: {self.card_number}")

    def check_count(self):

        try:
            user_count = int(self.entry.get())
            if user_count == self.running_count:
                self.result_label.config(text="Correct!", fg="green")
            else:
                self.result_label.config(text=f"Incorrect. The correct count is {self.running_count}", fg="red")
        except ValueError:
            self.result_label.config(text="Please enter a valid number.", fg="red")

    def toggle_auto_play(self):

        if self.auto_playing:
            self.auto_playing = False
            self.auto_play_button.config(text="Start Auto-Play")
        else:
            self.auto_playing = True
            self.auto_play_button.config(text="Stop Auto-Play")
            self.auto_play()

    def auto_play(self):

        if self.auto_playing:
            self.show_new_card()
            try:
                speed = int(self.speed_entry.get())
            except ValueError:
                speed = 1000
            self.root.after(speed, self.auto_play)

    def restart(self):

        self.card_number = 0
        self.running_count = 0
        self.auto_playing = False
        self.start_time = None
        self.card_times = []
        self.generate_deck()


        self.display_face_down_card()

        self.result_label.config(text="")
        self.card_number_label.config(text="Card Number: 0")
        self.auto_play_button.config(text="Start Auto-Play")

    def display_face_down_card(self):

        try:

            face_down_image = Image.open(resource_path("cards/face_down.png"))
            face_down_image = face_down_image.resize((150, 200))
            face_down_photo = ImageTk.PhotoImage(face_down_image)
            self.card_image_label.config(image=face_down_photo)
            self.card_image_label.image = face_down_photo
        except FileNotFoundError:
            self.card_image_label.config(text="Face down image not found", font=("Helvetica", 16))

    def show_stats(self):

        if not self.card_times:
            self.stats_label.config(text="No data available for stats.", fg="red")
            return

        total_time = sum(self.card_times)
        avg_time = total_time / len(self.card_times)
        max_time = max(self.card_times)
        min_time = min(self.card_times)

        stats_message = (
            f"Deck Count: {self.deck_count}\n"
            f"Cards Shown: {self.card_number}\n"
            f"Total Time: {total_time:.2f} seconds\n"
            f"Average Time per Card: {avg_time:.2f} seconds\n"
            f"Max Time per Card: {max_time:.2f} seconds\n"
            f"Min Time per Card: {min_time:.2f} seconds\n"
            f"Running Count: {self.running_count}"
        )

        self.stats_label.config(text=stats_message, fg="blue")

    def show_answer_options(self):

        correct_answer = self.running_count
        incorrect_answers = set()


        while len(incorrect_answers) < 6:
            random_answer = correct_answer + random.randint(-5, 5)
            if random_answer != correct_answer:
                incorrect_answers.add(random_answer)


        answer_options = list(incorrect_answers) + [correct_answer]
        random.shuffle(answer_options)


        for button in self.answer_buttons:
            button.destroy()

        self.answer_buttons.clear()


        for idx, answer in enumerate(answer_options):
            button = tk.Button(self.root, text=str(answer), command=lambda a=answer: self.check_answer(a),
                               font=("Helvetica", 14), bg="#8BC34A", fg="white", relief="raised", bd=5)
            button.place(x=60 + 40 * idx, y=450)
            self.answer_buttons.append(button)

    def check_answer(self, answer):

        if answer == self.running_count:
            self.result_label.config(text="Correct!", fg="green")
        else:
            self.result_label.config(text=f"Incorrect. The correct count is {self.running_count}", fg="red")


if __name__ == "__main__":
    root = tk.Tk()
    trainer = CardCountingTrainer(root)
    root.mainloop()
