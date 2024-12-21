import tkinter as tk
import random

# Значения карт для подсчета по системе Hi-Lo
CARD_VALUES = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

CARDS = list(CARD_VALUES.keys())

class CardCountingTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Counting Trainer")

        self.current_card = None
        self.running_count = 0

        # Карточный интерфейс
        self.card_label = tk.Label(root, text="", font=("Helvetica", 48))
        self.card_label.pack(pady=20)

        self.count_label = tk.Label(root, text="Running Count: 0", font=("Helvetica", 16))
        self.count_label.pack(pady=10)

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

    def show_new_card(self):
        """Показать новую карту и обновить счет."""
        self.current_card = random.choice(CARDS)
        self.running_count += CARD_VALUES[self.current_card]
        self.card_label.config(text=self.current_card)
        self.result_label.config(text="")

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

if __name__ == "__main__":
    root = tk.Tk()
    trainer = CardCountingTrainer(root)
    root.mainloop()
