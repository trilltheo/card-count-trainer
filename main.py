import tkinter as tk
from PIL import Image, ImageTk
import random
import time

# Значения карт для подсчета по системе Hi-Lo
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

        self.current_card = None
        self.card_number = 0
        self.running_count = 0
        self.auto_playing = False

        self.deck_count = 1
        self.deck = []
        self.generate_deck()

        self.start_time = None
        self.card_times = []

        # Карточный интерфейс
        self.card_image_label = tk.Label(root)
        self.card_image_label.pack(pady=20)

        self.card_number_label = tk.Label(root, text="Card Number: 0", font=("Helvetica", 16))
        self.card_number_label.pack(pady=10)

        # Кнопка для показа новой карты
        self.new_card_button = tk.Button(root, text="Show New Card", command=self.show_new_card)
        self.new_card_button.pack(pady=10)

        # Поле ввода для проверки подсчета
        self.entry = tk.Entry(root, font=("Helvetica", 16))
        self.entry.pack(pady=10)

        self.check_button = tk.Button(root, text="Check Count", command=self.check_count)
        self.check_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.result_label.pack(pady=10)

        # Автопролистывание
        self.auto_play_button = tk.Button(root, text="Start Auto-Play", command=self.toggle_auto_play)
        self.auto_play_button.pack(pady=10)

        self.speed_label = tk.Label(root, text="Speed (ms):", font=("Helvetica", 12))
        self.speed_label.pack()

        self.speed_entry = tk.Entry(root, font=("Helvetica", 12))
        self.speed_entry.insert(0, "1000")
        self.speed_entry.pack(pady=5)

        # Выбор количества колод
        self.deck_label = tk.Label(root, text="Number of Decks (1-8):", font=("Helvetica", 12))
        self.deck_label.pack()

        self.deck_entry = tk.Entry(root, font=("Helvetica", 12))
        self.deck_entry.insert(0, "1")
        self.deck_entry.pack(pady=5)

        self.set_deck_button = tk.Button(root, text="Set Deck Count", command=self.set_deck_count)
        self.set_deck_button.pack(pady=10)

        # Кнопка рестарта
        self.restart_button = tk.Button(root, text="Restart", command=self.restart)
        self.restart_button.pack(pady=10)

        # Кнопка для отображения статистики
        self.stats_button = tk.Button(root, text="Show Stats", command=self.show_stats)
        self.stats_button.pack(pady=10)

        # Кнопка для показа вариантов ответов
        self.show_answer_button = tk.Button(root, text="Show Answer Options", command=self.show_answer_options)
        self.show_answer_button.pack(pady=10)

        # Список для хранения кнопок вариантов ответа
        self.answer_buttons = []

    def generate_deck(self):
        """Создает колоду на основе количества выбранных колод."""
        self.deck = [f"{card}_of_{suit}" for card in CARDS for suit in SUITS] * self.deck_count
        random.shuffle(self.deck)

    def set_deck_count(self):
        """Устанавливает количество колод и перезапускает игру."""
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
        """Показать новую карту и обновить счет."""
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

        # Загрузка изображения карты
        try:
            card_image = Image.open(f"cards/{card}.png")
            card_image = card_image.resize((150, 200))
            card_photo = ImageTk.PhotoImage(card_image)
            self.card_image_label.config(image=card_photo)
            self.card_image_label.image = card_photo
        except FileNotFoundError:
            self.card_image_label.config(text="Image not found", font=("Helvetica", 16))

        self.result_label.config(text="")
        self.card_number_label.config(text=f"Card Number: {self.card_number}")

    def show_answer_options(self):
        """Показать 7 вариантов ответа."""
        self.result_label.config(text="Choose the correct running count:", fg="blue")

        # Генерация вариантов ответов
        correct_answer = self.running_count
        answer_choices = [correct_answer]

        # Добавление 6 неправильных вариантов
        while len(answer_choices) < 7:
            fake_answer = correct_answer + random.randint(-10, 10)
            if fake_answer not in answer_choices:
                answer_choices.append(fake_answer)

        random.shuffle(answer_choices)

        # Удаление старых кнопок, если они есть
        for button in self.answer_buttons:
            button.destroy()

        self.answer_buttons = []
        for i, answer in enumerate(answer_choices):
            button = tk.Button(self.root, text=str(answer), command=lambda ans=answer: self.check_answer(ans))
            button.pack(pady=5)
            self.answer_buttons.append(button)

    def check_answer(self, selected_answer):
        """Проверка выбранного ответа."""
        if selected_answer == self.running_count:
            self.result_label.config(text="Correct!", fg="green")
        else:
            self.result_label.config(text=f"Incorrect. The correct count is {self.running_count}", fg="red")

    def check_count(self):
        """Проверить правильность текущего счета."""
        try:
            user_count = int(self.entry.get())
            if user_count == self.running_count:
                self.result_label.config(text="Correct!", fg="green")
            else:
                self.result_label.config(text=f"Incorrect. The correct count is {self.running_count}", fg="red")
        except ValueError:
            self.result_label.config(text="Please enter a valid number.", fg="red")

    def toggle_auto_play(self):
        """Включить или выключить автопролистывание."""
        if self.auto_playing:
            self.auto_playing = False
            self.auto_play_button.config(text="Start Auto-Play")
        else:
            self.auto_playing = True
            self.auto_play_button.config(text="Stop Auto-Play")
            self.auto_play()

    def auto_play(self):
        """Реализация автопролистывания карт."""
        if self.auto_playing:
            self.show_new_card()
            try:
                speed = int(self.speed_entry.get())
            except ValueError:
                speed = 1000  # Значение по умолчанию
            self.root.after(speed, self.auto_play)

    def restart(self):
        """Перезапустить тренировку."""
        self.card_number = 0
        self.running_count = 0
        self.auto_playing = False
        self.start_time = None
        self.card_times = []
        self.generate_deck()
        self.card_image_label.config(image="")
        self.card_image_label.image = None
        self.result_label.config(text="")
        self.card_number_label.config(text="Card Number: 0")
        self.auto_play_button.config(text="Start Auto-Play")

    def show_stats(self):
        """Отображает статистику тренировки."""
        if not self.card_times:
            self.result_label.config(text="No data available for stats.", fg="red")
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

        self.result_label.config(text=stats_message, fg="blue")

if __name__ == "__main__":
    root = tk.Tk()
    trainer = CardCountingTrainer(root)
    root.mainloop()
