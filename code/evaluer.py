import csv, json, os, re, sys, time
from classifieur import CONSIGNE, classer
from evaluation import afficher_rapport

PAUSE = 2.1
BASE = os.path.join(os.path.dirname(__file__), "..")


def charger(chemin=os.path.join(BASE, "data", "tickets.csv")):
    with open(chemin, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def evaluer(modele, lignes, consigne=CONSIGNE, etiquette=None):
    etiquette = etiquette or modele
    vrais, predits, debut = [], [], time.time()
    for i, ligne in enumerate(lignes, 1):
        predits.append(classer(ligne["texte"], modele, consigne=consigne))
        vrais.append(ligne["categorie"])
        print(f"\r{i}/{len(lignes)}", end="", flush=True)
        time.sleep(PAUSE)
    resume = afficher_rapport(etiquette, vrais, predits)
    resume.update(modele=modele, etiquette=etiquette,
                  duree_s=round(time.time() - debut, 1),
                  predits=predits, vrais=vrais,
                  ids=[l["id"] for l in lignes])
    nom = re.sub(r"[^A-Za-z0-9.+-]+", "_", etiquette) + ".json"
    os.makedirs(os.path.join(BASE, "resultats"), exist_ok=True)
    with open(os.path.join(BASE, "resultats", nom), "w", encoding="utf-8") as f:
        json.dump(resume, f, ensure_ascii=False, indent=2)
    return resume


if __name__ == "__main__":
    evaluer(sys.argv[1], charger())
