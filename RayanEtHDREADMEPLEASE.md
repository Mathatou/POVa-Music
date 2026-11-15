
# Contrat d'interface : suivi des mains
 
Ce document décrit ce que le module de suivi (`tracking.py`) fournit au reste du projet.
 
## `tracker.get_hands()`
 
Renvoie toujours un objet `Hands`, défini dans `tracking.py`. Il contient deux objets `Hand` optionnels :
 
- `hands.pitch` : la main qui contrôle la hauteur de la note
- `hands.volume` : la main qui contrôle le volume
**Optionnel** signifie que si une main n'est pas détectée, le champ correspondant vaut `None`. Il faut donc toujours tester `is None` avant d'utiliser une main :
 
```python
hands = tracker.get_hands()
if hands.pitch is not None:
    zone = get_zone_index(hands.pitch.y)
```
 
Chaque rôle peut être `None` indépendamment de l'autre (une seule main visible, aucune main, etc.).
 
## Contenu d'une `Hand`
 
| Champ | Type | Description |
|---|---|---|
| `x` | `float` | Position horizontale, normalisée entre 0 et 1 |
| `y` | `float` | Position verticale, normalisée entre 0 et 1 |
| `is_fist` | `bool` | `True` si la main est un poing fermé |
 
### `y`
 
Normalisé entre 0 et 1, avec **0 en haut** de l'image.
 
### `x`
 
Normalisé entre 0 et 1, et issu de l'image **non retournée**.
 
Avec OpenCV, l'image affichée à l'écran est retournée (effet miroir) grâce à la fonction `flip`. Le `x` provient de la première image, avant ce retournement. Il est donc inversé par rapport à ce que voit l'utilisateur à l'écran.
 
### `is_fist`
 
Calculée pour les deux mains.
 
## `get_zone_index(y)`
 
Définie dans `zones.py`. Prend un `y` normalisé et renvoie le numéro de zone, de **0 en bas** à **11 en haut** de l'image.
