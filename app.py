#from flask import Flask, request, jsonify, render_template
import joblib
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="SpamClassifier",
    description="Application permettant de détecter un spam",
    version="1.0.0"
    )

#app = FastAPI(__name__)

model = joblib.load('training/spam_model.pkl')
vectorizer = joblib.load('training/vectorizer.pkl')

templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    message: str


@app.get('/')
def home(request: Request):
    '''
    Chemin racine, renvoie index.html
    '''
    return templates.TemplateResponse("index.html", {"request": request})


@app.post('/predict')
def predict(item:Item):
    '''
    Fait la prédiction, nécéssite une json au format {'message' : "Mon message ou mon SMS"}
    '''
    
    message = item.message

    message_vectorized = vectorizer.transform([message])

    prediction = model.predict(message_vectorized)

    result = 'Your message is a spam' if prediction[0] == 1 else 'Your messsage is a ham'
    return {'prediction': result}

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")