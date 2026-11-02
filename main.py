from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from schemas import QuestionModele
from services import envoyer_question, obtenir_modeles


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Accueil de l'API
@app.get("/")
async def accueil():
    return {"message": "Bienvenue dans mon API IA !"}

# Poser une question à l'IA
@app.post("/question")
async def question(data: QuestionModele):
    try:
        reponse = await envoyer_question(data.question, data.modele)
        return {"question": data.question, "modele": data.modele,"reponse": reponse}

    except Exception as erreur:
        raise HTTPException(status_code=500, detail=str(erreur))


# Afficher les modèles disponibles
@app.get("/models")
async def afficher_modeles():
    try:
        modeles = await obtenir_modeles()
        return {"modeles": modeles}
    except Exception as erreur:
        raise HTTPException(status_code=500, detail=str(erreur))


# Afficher la page HTML
@app.get("/app")
async def afficher_page(request: Request):
    modeles = await obtenir_modeles()
    return templates.TemplateResponse(request=request,name="index.html",context={"modeles": modeles,"reponse": None,"modele_selectionne": None})

# Envoyer une question depuis le formulaire
@app.post("/interface/question")
async def envoyer_formulaire(request: Request,question: str = Form(...),modele: str = Form(...)):
    try:
        reponse = await envoyer_question(question, modele)
    except Exception as erreur:
        reponse = f"Erreur : {erreur}"
    modeles = await obtenir_modeles()
    return templates.TemplateResponse(request=request,name="index.html",context={"modeles": modeles,"reponse": reponse,"modele_selectionne": modele})
