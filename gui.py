

import tkinter as tk
from tkinter import messagebox
from config import BASE_ATTEMPTS, BASE_HINTS
from game_logic import GameState
from recommender import RecommendationEngine

class WordGuessGUI:
    def __init__(self, root, words):
        self.root = root
        self.words = words
        self.recommender = RecommendationEngine()

        self.root.title("Word Guess Game")
        self.root.geometry("520x620")
        self.root.resizable(False, False)

        self.create_widgets()
        self.start_game()

    def create_widgets(self):
        tk.Label(self.root, text="🎯 WORD GUESS GAME",
                 font=("Arial", 20, "bold")).pack(pady=10)

        self.word_label = tk.Label(self.root, font=("Courier", 26))
        self.word_label.pack(pady=20)

        self.info_label = tk.Label(self.root)
        self.info_label.pack()

        self.msg_label = tk.Label(self.root)
        self.msg_label.pack(pady=5)

        self.buttons = {}
        frame = tk.Frame(self.root)
        frame.pack()

        for i, ch in enumerate("abcdefghijklmnopqrstuvwxyz"):
            btn = tk.Button(frame, text=ch.upper(), width=4,
                            command=lambda c=ch: self.make_guess(c))
            btn.grid(row=i//7, column=i%7, padx=3, pady=3)
            self.buttons[ch] = btn

        tk.Button(self.root, text="💡 Hint", command=self.use_hint).pack(pady=10)
        tk.Button(self.root, text="🔄 Restart", command=self.start_game).pack()

    def start_game(self):
        self.recommender.games_played += 1
        word, difficulty = self.recommender.choose_word(self.words)
        self.state = GameState(word, BASE_ATTEMPTS, BASE_HINTS)

        for btn in self.buttons.values():
            btn.config(state=tk.NORMAL)

        self.msg_label.config(text=f"Recommended Difficulty: {difficulty}")
        self.update_display()

    def update_display(self):
        self.word_label.config(text=" ".join(self.state.progress))
        self.info_label.config(
            text=f"Attempts: {self.state.attempts} | Hints: {self.state.hints}"
        )

    def make_guess(self, letter):
        result = self.state.guess_letter(letter)
        self.buttons[letter].config(state=tk.DISABLED)

        if result is False:
            self.msg_label.config(text="❌ Wrong Guess")
        elif result is True:
            self.msg_label.config(text="✅ Correct Guess")

        self.update_display()
        self.check_status()

    def use_hint(self):
        letter = self.state.use_hint()
        if letter:
            self.buttons[letter].config(state=tk.DISABLED)
            self.msg_label.config(text=f"💡 Hint revealed: {letter.upper()}")
            self.update_display()

    def check_status(self):
        if self.state.is_won():
            self.recommender.games_won += 1
            messagebox.showinfo("Win", f"You won! Word: {self.state.word}")
        elif self.state.is_lost():
            messagebox.showerror("Lose", f"Word was: {self.state.word}")
