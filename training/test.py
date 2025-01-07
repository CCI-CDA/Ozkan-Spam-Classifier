import joblib

model = joblib.load('spam_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

new_message = ["Free entry to win FA Cup tickets! Text now to claim your prize"]

new_message_vectorized = vectorizer.transform(new_message)

prediction = model.predict(new_message_vectorized)
print("Spam" if prediction[0] == 1 else "Ham")