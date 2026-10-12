import glob, json, os
BASE = os.path.join(os.path.dirname(__file__), "..")
res = [json.load(open(f, encoding="utf-8"))
       for f in sorted(glob.glob(os.path.join(BASE, "resultats", "*.json")))]
n = len(res[0]["vrais"])
for r in res:
    r["corrects"] = round(r["accuracy"] * n)
base = sorted([r for r in res if "+" not in r["etiquette"]],
              key=lambda r: -r["macro_f1"])
var = [r for r in res if "+" in r["etiquette"]]
b1, b2 = base[0], base[1]
ecart_t = b1["corrects"] - b2["corrects"]
ecart_p = 100 * (b1["macro_f1"] - b2["macro_f1"])
faible = min(b1["par_classe"].items(), key=lambda kv: kv[1]["f1"])
conf = max(((v, p, k) for v, l in b1["matrice"].items()
            for p, k in l.items() if p != v), key=lambda x: x[2])
txt = f"""FICHE DE DÉCISION
Tâche et jeu de test : router les tickets vers 4 équipes ; {n} tickets annotés, classes déséquilibrées
Métrique de décision : macro-F1, choisie avant de voir les résultats
Candidats évalués : {', '.join(r['etiquette'] for r in res)}
Modèle retenu et son score : {b1['etiquette']} (macro-F1 = {b1['macro_f1']:.3f}, accuracy = {b1['accuracy']:.3f})
Écart avec le deuxième ({b2['etiquette']}) : {ecart_p:.1f} points = {ecart_t} tickets -> {'différence mesurable' if ecart_t >= 5 else 'pas de différence mesurable (< 5 tickets)'}
Catégorie la plus faible : {faible[0]} (F1 = {faible[1]['f1']:.3f})
Confusion principale : {conf[0]} envoyé vers {conf[1]} ({conf[2]} tickets)
Latence : {b1['duree_s']} s pour {n} tickets ; autres : {', '.join(f"{r['etiquette']} {r['duree_s']} s" for r in base[1:])}
Tickets invalides : {b1['taux_invalides']:.3f}
"""
for v in var:
    d = v["corrects"] - b1["corrects"]
    txt += f"Effet des 4 exemples ({v['etiquette']}) : {d:+d} tickets, macro-F1 {v['macro_f1'] - b1['macro_f1']:+.3f}\n"
txt += "Risque identifié : (à écrire toi-même)\n"
txt += "Recommandation : (à écrire toi-même)\n"
open(os.path.join(BASE, "fiche_decision.md"), "w", encoding="utf-8").write(txt)
print(txt)
