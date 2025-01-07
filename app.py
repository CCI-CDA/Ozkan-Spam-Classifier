from flask import Flask, request, jsonify, render_template
import joblib

app = Flask(__name__)

model = joblib.load('training/spam_model.pkl')
vectorizer = joblib.load('training/vectorizer.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if 'message' not in data:
        return jsonify({'error': 'Message not provided'}), 400

    message = data['message']

    message_vectorized = vectorizer.transform([message])

    prediction = model.predict(message_vectorized)

    result = 'Your message is a spam' if prediction[0] == 1 else 'Your messsage is a ham'
    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True)
