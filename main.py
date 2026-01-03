
import tkinter as tk
from word_loader import load_words
from gui import WordGuessGUI

def main():
    words = load_words()
    root = tk.Tk()
    WordGuessGUI(root, words)
    root.mainloop()

if __name__ == "__main__":
    main()
