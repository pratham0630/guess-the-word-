

from wordfreq import top_n_list

def load_words(limit=50000):
    words = top_n_list("en", limit)
    return [w for w in words if w.isalpha()]
