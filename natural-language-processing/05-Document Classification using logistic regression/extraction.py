from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

documents = [
    "exam timetable is announced",
    "project submission deadline",
    "college annual function",
    "sports day celebration",
    "results will be declared soon",
    "cultural fest invitation"
]

labels = [0, 0, 1, 1, 0, 1]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents)
model = LogisticRegression()
model.fit(X, labels)

test_docs = ["annual function details", "exam deadline"]
X_test = vectorizer.transform(test_docs)
predictions = model.predict(X_test)
print("Predictions:", predictions)
