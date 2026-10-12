import glob, json, os
BASE = os.path.join(os.path.dirname(__file__), "..")
fichiers = sorted(glob.glob(os.path.join(BASE, "resultats", "*.json")))
res = [json.load(open(f, encoding="utf-8")) for f in fichiers]
if not res:
    raise SystemExit("Aucun résultat dans resultats/")
n = len(res[0]["vrais"])
for r in res:
    r["corrects"] = round(r["accuracy"] * n)
meilleur = max(r["corrects"] for r in res)
print(f"{'Modèle':<36}{'accuracy':>9}{'macro-F1':>9}{'Corrects':>9}{'Écart(t)':>9}{'Durée(s)':>9}")
for r in sorted(res, key=lambda r: -r["macro_f1"]):
    print(f"{r['etiquette']:<36}{r['accuracy']:>9.3f}{r['macro_f1']:>9.3f}"
          f"{r['corrects']:>9}{meilleur - r['corrects']:>9}{r['duree_s']:>9}")
print("\nRègle : il faut au moins 5 tickets d'écart pour parler de différence.")
print("\nTickets où les modèles divergent :")
ids = res[0]["ids"]
for i, tid in enumerate(ids):
    preds = [r["predits"][i] for r in res]
    if len(set(preds)) > 1:
        detail = " | ".join(f"{r['etiquette'][:20]}={p}" for r, p in zip(res, preds))
        print(f"{tid} (vrai : {res[0]['vrais'][i]}) -> {detail}")
