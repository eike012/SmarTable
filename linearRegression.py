import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

stopWords_pt = set(stopwords.words('portuguese'))

data = pd.read_csv('dataset.csv')

tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words=list(stopWords_pt))
X = tfidf_vectorizer.fit_transform(data['Text'])

X_train, X_test, y_train, y_test = train_test_split(X, data['Category'], test_size=0.2, random_state=42)


classifier = LogisticRegression()
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
print(f"Accuracy: {accuracy}")
print(report)
