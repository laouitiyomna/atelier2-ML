import sys
from classifieur import CONSIGNE_EXEMPLES
from evaluer import charger, evaluer
modele = sys.argv[1]
evaluer(modele, charger(), consigne=CONSIGNE_EXEMPLES,
        etiquette=f"{modele} + 4 exemples")
