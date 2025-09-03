# metrics.py
# Implements all metrics described in Text-Analysis.docx:
# - Positive/Negative scores (dictionary-based)
# - Polarity, Subjectivity
# - Average Sentence Length, % Complex Words, Fog Index
# - Complex Word Count, Word Count (stopwords removed), Syllables per Word
# - Personal Pronouns, Average Word Length

import os
import re
from nltk.tokenize import sent_tokenize, word_tokenize

# Absolute paths to dictionaries and stopword lists
POSITIVE_DICT = r"C:\Users\91897\OneDrive\Desktop\Text Analysis\Original\MasterDictionary\positive-words.txt"
NEGATIVE_DICT = r"C:\Users\91897\OneDrive\Desktop\Text Analysis\Original\MasterDictionary\negative-words.txt"
STOPWORDS_DIR = r"C:\Users\91897\OneDrive\Desktop\Text Analysis\Original\StopWords"

def load_word_list(path, encoding="ISO-8859-1"):
    """
    Load a list of words from a file, lowercased, skipping comments/blank lines.
    Returns a set for O(1) lookups.
    """
    with open(path, "r", encoding=encoding) as f:
        return set(w.strip().lower() for w in f if w.strip() and not w.startswith(";"))

# Load positive and negative word dictionaries (as sets)
positive_words = load_word_list(POSITIVE_DICT)
negative_words = load_word_list(NEGATIVE_DICT)

# Merge all stopword files into one set
stopwords = set()
for file in os.listdir(STOPWORDS_DIR):
    if file.endswith(".txt"):
        stopwords |= load_word_list(os.path.join(STOPWORDS_DIR, file))

def clean_and_tokenize(text):
    """
    Tokenize into words and keep only alphabetic tokens, lowercased.
    Used as the base for most metrics.
    """
    words = word_tokenize(text)
    return [w.lower() for w in words if w.isalpha()]

def positive_score(words):
    """Count of tokens present in the positive dictionary."""
    return sum(1 for w in words if w in positive_words)

def negative_score(words):
    """Count of tokens present in the negative dictionary."""
    return sum(1 for w in words if w in negative_words)

def polarity_score(pos, neg):
    """
    (Positive - Negative) / ((Positive + Negative) + epsilon)
    Range ~ [-1, 1]
    """
    return (pos - neg) / ((pos + neg) + 0.000001)

def subjectivity_score(pos, neg, total_words):
    """
    (Positive + Negative) / (Total words + epsilon)
    Higher means more subjective language.
    """
    return (pos + neg) / (total_words + 0.000001)

def syllable_count_per_word(word):
    """
    Approximate syllable counting:
    - Count vowel groups (aeiou)
    - Subtract 1 for words ending in 'es' or 'ed' when count > 1
    """
    word = word.lower()
    vowels = "aeiou"
    count, prev_vowel = 0, False
    for char in word:
        if char in vowels:
            if not prev_vowel:
                count += 1
            prev_vowel = True
        else:
            prev_vowel = False
    if word.endswith(("es", "ed")) and count > 1:
        count -= 1
    return count

def count_complex_words(words):
    """Complex words are those with > 2 syllables."""
    return sum(1 for w in words if syllable_count_per_word(w) > 2)

def avg_sentence_length(text):
    """
    Average sentence length = total words / total sentences.
    Sentences are identified via NLTK's sent_tokenize.
    """
    sentences = sent_tokenize(text)
    words = clean_and_tokenize(text)
    return len(words) / max(1, len(sentences))

def percentage_complex_words(words):
    """Percentage (0..1) of words that are complex."""
    return count_complex_words(words) / max(1, len(words))

def fog_index(avg_sent_len, pct_complex):
    """
    Gunning Fog Index = 0.4 * (Average Sentence Length + Percentage Complex Words * 100)
    """
    return 0.4 * (avg_sent_len + pct_complex * 100)

def word_count_excluding_stopwords(words):
    """
    Word Count metric (as per spec) often excludes stopwords.
    This function removes tokens that appear in the combined stopwords list.
    """
    return sum(1 for w in words if w not in stopwords)

def syllables_per_word(words):
    """Average syllables per token."""
    return sum(syllable_count_per_word(w) for w in words) / max(1, len(words))

def personal_pronouns(text):
    """
    Count occurrences of personal pronouns:
    I, we, my, ours, us (case-insensitive). 'US' (country) is naturally excluded by word boundaries.
    """
    regex = r"\b(I|we|my|ours|us)\b"
    matches = re.findall(regex, text, flags=re.I)
    return len(matches)

def avg_word_length(words):
    """Average number of characters per word."""
    return sum(len(w) for w in words) / max(1, len(words))
