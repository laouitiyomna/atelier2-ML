import json, os, time
from groq import Groq, RateLimitError, BadRequestError

CATEGORIES = ["facturation", "technique", "compte", "commercial"]
client = Groq(api_key=os.environ["GROQ_API_KEY"])

CONSIGNE = """Tu es un agent de tri du service client.
Classe le ticket dans exactement une catégorie :
- facturation : montant, facture, paiement, remboursement.
- technique : un service ne fonctionne pas comme prévu.
- compte : accès au compte ou données personnelles.
- commercial : choix d'offre, abonnement, résiliation.
Si plusieurs catégories semblent possibles, retiens l'intention
principale du client : ce qu'il veut obtenir.
Réponds uniquement par un objet JSON de la forme
{"categorie": "<une des quatre>"}."""

CONSIGNE_EXEMPLES = CONSIGNE + """
Exemples :
"Le geste commercial promis n'est pas sur mon relevé." ->
 {"categorie": "facturation"}
"Je paie chaque mois et rien ne marche depuis jeudi." ->
 {"categorie": "technique"}
"Mon associé doit consulter les mêmes documents." ->
 {"categorie": "compte"}
"Je déménage à l'étranger en septembre." ->
 {"categorie": "commercial"}"""


def classer(texte, modele, consigne=CONSIGNE, temperature=0.0):
    reponse = None
    for tentative in range(6):
        try:
            reponse = client.chat.completions.create(
                model=modele,
                temperature=temperature,
                response_format={"type": "json_object"},
                messages=[{"role": "system", "content": consigne},
                          {"role": "user", "content": texte}],
            )
            break
        except RateLimitError:
            time.sleep(10 * (tentative + 1))
        except BadRequestError:
            return "invalide"
    if reponse is None:
        return "invalide"
    try:
        categorie = json.loads(
            reponse.choices[0].message.content).get("categorie", "")
    except (json.JSONDecodeError, AttributeError, TypeError):
        return "invalide"
    categorie = str(categorie).strip().lower()
    return categorie if categorie in CATEGORIES else "invalide"
