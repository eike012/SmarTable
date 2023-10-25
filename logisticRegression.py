import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from nltk.corpus import stopwords

import nltk
nltk.download('stopwords')

stopWords_pt = set(stopwords.words('portuguese'))
data = pd.read_csv('dataset.csv')
tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words=list(stopWords_pt))

def train():
    X = tfidf_vectorizer.fit_transform(data['Text'])

    X_train,_, y_train,_ = train_test_split(X, data['Category'], test_size=0.2, random_state=42)


    classifier = LogisticRegression()
    classifier.fit(X_train, y_train)

    joblib.dump(classifier, 'classifier.pkl')
