import re

def extraire_contenu(texte):
    # Utiliser une expression régulière pour capturer le contenu entre les premiers guillemets
    pattern = r'"(.*?)"'
    match = re.search(pattern, texte)
    if match:
        return match.group(1)  # Retourner le contenu capturé
    return None  # Retourner None si aucun match n'est trouvé

# Exemple d'utilisation
texte = 'Bonjour, voici une chaîne avec "un contenu intéressant" à extraire et a "ne pas extraire".'
resultat = extraire_contenu(texte)
print(resultat)  # Affiche : un contenu intéressant
