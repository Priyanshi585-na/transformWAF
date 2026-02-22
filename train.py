import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.model_selection import train_test_split


df = pd.read_csv('data/combined_dataset.csv', sep="|", engine = "python")
x = df['processed_log']
y = df['classification']

x_train,x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(
    ngram_range=(1,2),
    analyzer='char_wb',
    max_features=50000
)

x_train_vec = vectorizer.fit_transform(x_train)
joblib.dump(vectorizer, 'artifacts/vectorizer.pkl')

model = LogisticRegression(max_iter=200)
model.fit(x_train_vec, y_train)

joblib.dump(model, 'artifacts/lr_model.pkl')



