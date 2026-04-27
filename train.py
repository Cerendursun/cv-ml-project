from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

texts = [
    "python machine learning data science sql",
    "html css javascript frontend developer",
    "excel office management reporting",
    "deep learning ai neural networks python",
    "react frontend developer javascript",
]

labels = [90, 70, 50, 95, 75]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model hazır!")