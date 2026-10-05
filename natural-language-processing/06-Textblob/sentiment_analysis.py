from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

text = input("Enter a few sentences: ")
sentences = text.split(".")

for sentence in sentences:
    if sentence.strip():
        score = analyzer.polarity_scores(sentence)
        print(sentence.strip())
        print(score)
        print()
