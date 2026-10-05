import nltk
from nltk import word_tokenize, bigrams, trigrams
from collections import Counter

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

text = input("Enter training text: ")
tokens = word_tokenize(text.lower())

bigram_counts = Counter(bigrams(tokens))
trigram_counts = Counter(trigrams(tokens))

test_text = input("Enter sentence to evaluate: ")
test_tokens = word_tokenize(test_text.lower())
test_trigrams = list(trigrams(test_tokens))

probability = 1.0

for w1, w2, w3 in test_trigrams:
    bg_count = bigram_counts[(w1, w2)]
    if bg_count > 0:
        probability *= trigram_counts[(w1, w2, w3)] / bg_count
    else:
        probability = 0.0

print("Trigrams:", test_trigrams)
print("Probability:", probability)
