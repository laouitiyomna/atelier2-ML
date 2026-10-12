import csv, os
from collections import Counter
CHEMIN = os.path.join(os.path.dirname(__file__), "..", "data", "tickets.csv")
with open(CHEMIN, encoding="utf-8") as f:
    lignes = list(csv.DictReader(f))
for cat, n in Counter(l["categorie"] for l in lignes).most_common():
    print(f"{cat:<13}{n:>3} {100*n/len(lignes):>5.1f} % {'#' * n}")
