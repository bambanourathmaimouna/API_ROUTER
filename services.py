import httpx
from config import key

URL = "https://openrouter.ai/api/v1"

instructions = """
    Tu es un assistant intelligent.
    Tu dois toujours répondre par la langue utiliser par l'utilisateur.
    Tu dois donner des réponses simples et faciles à comprendre.
    Tu dois expliquer les sujets étape par étape.
    Si tu ne connais pas une réponse, dis-le clairement.
    """

async def envoyer_question(question: str, modele: str):
    async with httpx.AsyncClient() as client:
        reponse = await client.post(f"{URL}/chat/completions",headers={"Authorization": f"Bearer {key}"},
            json={
                "model": modele,
                "messages": [{"role": "user", "content": question},{"role":"system","content": instructions}]
                })
    resultat = reponse.json()
    if reponse.status_code != 200:
        raise Exception(resultat["error"]["message"])
    return resultat["choices"][0]["message"]["content"]


async def obtenir_modeles():
    async with httpx.AsyncClient() as client:
        reponse = await client.get(f"{URL}/models",headers={"Authorization": f"Bearer {key}"})
    resultat = reponse.json()
    modeles = []
    for modele in resultat["data"]:
        if modele["id"].endswith(":free"):
            modeles.append({"id": modele["id"],"nom": modele["name"]})
    return modeles
