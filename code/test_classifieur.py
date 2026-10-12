from classifieur import classer
modele = "openai/gpt-oss-20b"
tests = ["Ma facture est trop élevée",
         "Je ne peux plus me connecter à mon compte",
         "L'application ne fonctionne plus",
         "Je souhaite changer mon abonnement",
         " bonjour ! "]
for texte in tests:
    print(f"Ticket : {texte}")
    print(f"Catégorie : {classer(texte, modele)}\n")
