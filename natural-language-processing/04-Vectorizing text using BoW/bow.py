from sklearn.feature_extraction.text import CountVectorizer

documents = [
    "data science is fun and exciting",
    "natural language processing is part of data science",
    "python is great for data science"
]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents)

print("Vocabulary:", vectorizer.get_feature_names_out())
print("BoW Representation Matrix:")
print(X.toarray())
