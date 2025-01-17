#from flask import Flask, request, jsonify, render_template
import joblib
from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import FastAPI, Request, Form, HTTPException, Response
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3
from passlib.context import CryptContext

db_path = "spams.db"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

app = FastAPI(
    title="SpamClassifier",
    description="Application permettant de détecter un spam",
    version="1.0.0"
    )

app.mount("/static", StaticFiles(directory="static"), name="static")
#app = FastAPI(__name__)

model = joblib.load('training/spam_model.pkl')
vectorizer = joblib.load('training/vectorizer.pkl')

templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    message: str

class User(BaseModel):
    nom : str
    password: str

class UserRegistration(BaseModel):
    nom: str = Field(..., min_length=2, max_length=50, pattern="^[a-zA-Z]+$")
    prenom: str = Field(..., min_length=2, max_length=50, pattern="^[a-zA-Z]+$")
    mdp: str = Field(..., min_length=8, max_length=128)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@app.post("/connexion")
async def login(nom: Annotated[str, Form()], mdp: Annotated[str, Form()], response: Response):

    cursor.execute("SELECT * FROM utilisateurs WHERE nom = ? AND mdp = ?", (nom, mdp))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Identifiants incorrects")

    # Rediriger vers la page d'accueil après connexion réussie
    redirect_response = RedirectResponse(url="/", status_code=302)
    redirect_response.set_cookie(key="session_token", value=nom, httponly=True)
    return redirect_response


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    session_token = request.cookies.get("session_token")
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "username": session_token}
    )


@app.post("/inscription")
async def inscription(nom: Annotated[str, Form()], prenom:Annotated[str, Form()], mdp: Annotated[str, Form()]):

    cursor.execute("SELECT COUNT(*) FROM utilisateurs WHERE nom = ?", [nom])
    if cursor.fetchone()[0] > 0:
        raise HTTPException(status_code=400, detail="Un utilisateur avec ce nom existe déjà")
    
    hashed_password = hash_password(mdp)

    cursor.execute("""INSERT INTO utilisateurs (nom, prenom, mdp) VALUES(?,?,?);""", [nom,prenom,hashed_password])
    conn.commit()
    redirect_response = RedirectResponse(url="/", status_code=302)
    redirect_response.set_cookie(key="session_token", value=nom, httponly=True)
    return redirect_response

@app.get("/deconnexion")
async def deconnexion(response: Response):
    # Supprimer le cookie de session
    response = RedirectResponse(url="/")
    response.delete_cookie("session_token")
    return response

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