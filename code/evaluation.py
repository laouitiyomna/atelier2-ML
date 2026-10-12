CATEGORIES = ["facturation", "technique", "compte", "commercial"]


def accuracy(vrais, predits):
    return sum(1 for v, p in zip(vrais, predits) if v == p) / len(vrais)


def scores_par_classe(vrais, predits, classes=CATEGORIES):
    resultat = {}
    for c in classes:
        vp = sum(1 for v, p in zip(vrais, predits) if v == c and p == c)
        fp = sum(1 for v, p in zip(vrais, predits) if v != c and p == c)
        fn = sum(1 for v, p in zip(vrais, predits) if v == c and p != c)
        precision = vp / (vp + fp) if (vp + fp) else 0.0
        recall = vp / (vp + fn) if (vp + fn) else 0.0
        f1 = (2 * precision * recall / (precision + recall)
              if (precision + recall) else 0.0)
        resultat[c] = {"precision": precision, "recall": recall,
                       "f1": f1, "support": vp + fn}
    return resultat


def f1_macro(scores):
    return sum(d["f1"] for d in scores.values()) / len(scores)


def taux_invalides(predits):
    return sum(1 for p in predits if p not in CATEGORIES) / len(predits)


def matrice_confusion(vrais, predits, classes=CATEGORIES):
    colonnes = list(classes) + ["invalide"]
    m = {v: {p: 0 for p in colonnes} for v in classes}
    for v, p in zip(vrais, predits):
        if v in m:
            m[v][p if p in colonnes else "invalide"] += 1
    return m


def afficher_rapport(etiquette, vrais, predits):
    scores = scores_par_classe(vrais, predits)
    m = matrice_confusion(vrais, predits)
    acc, mf1, inv = accuracy(vrais, predits), f1_macro(scores), taux_invalides(predits)
    print(f"\n=== {etiquette} ===")
    print(f"accuracy : {acc:.3f}")
    print(f"macro-F1 : {mf1:.3f}")
    print(f"invalides : {inv:.3f}")
    print(f"{'categorie':<13}{'precision':>10}{'recall':>8}{'F1':>8}{'n':>4}")
    for c, d in scores.items():
        print(f"{c:<13}{d['precision']:>10.3f}{d['recall']:>8.3f}"
              f"{d['f1']:>8.3f}{d['support']:>4}")
    print("\nConfusion matrix (lignes = vérité, colonnes = prédiction)")
    cols = list(next(iter(m.values())).keys())
    print(" " * 13 + "".join(f"{c[:6]:>7}" for c in cols))
    for v, ligne in m.items():
        print(f"{v:<13}" + "".join(f"{ligne[c]:>7}" for c in cols))
    return {"accuracy": acc, "macro_f1": mf1, "taux_invalides": inv,
            "par_classe": scores, "matrice": m}
