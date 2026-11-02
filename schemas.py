from pydantic import BaseModel

class QuestionModele(BaseModel):
    question : str
    modele : str