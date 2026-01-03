

class GameState:
    def __init__(self, word, attempts, hints):
        self.word = word
        self.progress = ["-"] * len(word)
        self.attempts = attempts
        self.hints = hints
        self.guessed_letters = set()

    def guess_letter(self, letter):
        if letter in self.guessed_letters:
            return None

        self.guessed_letters.add(letter)

        if letter in self.word:
            for i, ch in enumerate(self.word):
                if ch == letter:
                    self.progress[i] = letter
            return True
        else:
            self.attempts -= 1
            return False

    def use_hint(self):
        hidden = [i for i, ch in enumerate(self.progress) if ch == "-"]
        if not hidden or self.hints == 0:
            return None

        index = hidden[0]
        letter = self.word[index]
        self.hints -= 1
        self.guess_letter(letter)
        return letter

    def is_won(self):
        return "-" not in self.progress

    def is_lost(self):
        return self.attempts <= 0
