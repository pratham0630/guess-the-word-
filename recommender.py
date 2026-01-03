

from wordfreq import zipf_frequency
import random
from config import DIFFICULTY_CONFIG

class RecommendationEngine:
    def __init__(self):
        self.games_played = 0
        self.games_won = 0
        self.recent_words = []

    def recommend_difficulty(self):
        if self.games_played < 3:
            return "Easy"

        win_rate = self.games_won / self.games_played
        if win_rate >= 0.7:
            return "Hard"
        elif win_rate >= 0.4:
            return "Medium"
        return "Easy"

    def choose_word(self, words):
        difficulty = self.recommend_difficulty()
        cfg = DIFFICULTY_CONFIG[difficulty]

        candidates = [
            w for w in words
            if cfg["min_len"] <= len(w) <= cfg["max_len"]
            and zipf_frequency(w, "en") >= cfg["min_zipf"]
            and w not in self.recent_words
        ]

        word = random.choice(candidates)
        self.recent_words.append(word)
        if len(self.recent_words) > 10:
            self.recent_words.pop(0)

        return word, difficulty
