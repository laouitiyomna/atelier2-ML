FICHE DE DÉCISION

Tâche et jeu de test : router les tickets vers 4 équipes (facturation, technique, compte, commercial) ; 72 tickets annotés, classes déséquilibrées (22 / 20 / 16 / 14).

Métrique de décision : macro-F1, choisie avant de voir les résultats.

Candidats évalués (même jeu de test, même consigne, même parsing, température 0) :
- qwen/qwen3.8-27b : 69/72, macro-F1 0,956
- openai/gpt-oss-20b : 68/72, macro-F1 0,947
- openai/gpt-oss-120b : 66/72, macro-F1 0,920
- variante gpt-oss-20b + 4 exemples : 68/72, macro-F1 0,951

Modèle retenu et son score : openai/gpt-oss-20b (macro-F1 = 0,947 ; accuracy = 0,944 ; 68/72).

Écart avec le deuxième : le meilleur score est celui de qwen. Écart avec gpt-oss-20b : 0,9 point = 1 ticket. Écart maximal entre deux modèles : 3 tickets (3,6 points). C'est inférieur à 5 tickets : pas de différence mesurable.

Catégorie la plus faible (gpt-oss-20b) : commercial (F1 = 0,889). Confusions : un ticket commercial envoyé vers facturation et un ticket classé invalide. Les erreurs sont isolées : aucune confusion dominante.

Latence (pause de 2,1 s par ticket retirée) : gpt-oss-120b environ 45 s, gpt-oss-20b environ 51 s, qwen environ 85 s pour 72 tickets. Qwen est environ 1,7 fois plus lent pour un gain de 1 ticket.

Effet de la consigne avec 4 exemples : 0 ticket de gain (68/72 contre 68/72). Deux tickets corrigés (T006, T066), deux tickets cassés (T041, T057). Le levier n'est ni le modèle ni la consigne : on est au plafond de ce jeu de test.

Risque identifié :
- 72 tickets seulement : un ticket vaut 1,4 point, donc les écarts d'un à trois tickets sont du bruit.
- 5 textes coupés dans le PDF fourni (T016, T029, T033, T036, T057).
- Les tickets ambigus (T004, T040, T061) divergent selon les modèles : l'annotation elle-même est discutable.
- Pas de catégorie « autre » : un message comme « bonjour » est classé commercial.
- Quelques réponses invalides (1 sur 72 pour gpt-oss-20b) : à gérer en production.

Recommandation : les modèles sont séparés de moins de 5 tickets, donc la qualité n'est pas mesurablement différente. On retient gpt-oss-20b : plus petit que le 120b, plus rapide que qwen. Avant la mise en production, valider sur un plus grand jeu de test et ajouter une catégorie « autre ».
