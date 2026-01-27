# Testeur d’automates binaires

Un outil Python permettant de **modéliser, simuler et tester des automates finis déterministes (AFD) et non déterministes (AFN)** sur l’alphabet binaire `{0,1}`.  
Le projet vérifie automatiquement qu’un automate reconnaît correctement un langage binaire donné.

Dans la version actuelle, le projet permet :  

- de tester un **AFD classique** (ex. nombres congrus à 1 modulo 4),  
- de créer un **AFN**, puis de le **transformer en AFD** (déterminisation), même si certaines transitions sont absentes.  

---

## Objectifs

- Implémenter un **automate fini déterministe** (`Automate`) et un **automate fini non déterministe** (`AutomateAFN`).  
- Simuler la lecture de mots binaires et suivre les **états visités**.  
- Tester automatiquement un automate sur un grand nombre d’entrées, avec un **critère de reconnaissance généralisé**.  
- Vérifier la correspondance entre le langage et le comportement de l’automate.  
- Démontrer la **déterminisation d’un AFN partiel**, générant éventuellement un **état puits**.

---

## Principe théorique

### Automate déterministe exemple : `n % 4 == 1`

Un entier est congruent à **1 modulo 4** si et seulement si :  

- son écriture binaire se termine par `"01"`, ou  
- elle est `"1"` (pour le premier entier 1).  

L’automate implémenté exploite cette propriété et ne dépend que du **suffixe** du mot binaire.

| État | q0 (entrée 0) | q1 (entrée 1) | Final |
|------|---------------|---------------|-------|
| e0   | e0            | e1            | ❌    |
| e1   | e0            | e2            | ✅    |
| e2   | e0            | e2            | ❌    |

---

### Automate non déterministe exemple

- Reconnaît toutes les chaînes de longueur ≥ 3 ayant un `'1'` en **antépénultième position**.  
- Les états ont des **transitions multiples possibles** pour un même symbole (non déterminisme).  
- Exemple :

| État | 0 | 1 | Final |
|------|---|---|-------|
| e0   | {e0} | {e0, e1} | ❌ |
| e1   | {e2} | {e2} | ❌ |
| e2   | {e3} | {e3} | ❌ |
| e3   | {}   | {}   | ✅ |

---

### Déterminisation

- Transforme un **AFN partiel** en **AFD total**.  
- Si certaines transitions n’existent pas, un **état puits** est créé.  
- L’AFD résultant a une transition pour **tous les symboles de chaque état**.

---

## Tests automatisés

- `TestAutomate.tester_automate(critere, n_tests, afficher_premiers)` permet de tester un automate avec **n’importe quel critère**.  
- Exemple :

```python
# Critère modulo 4
def critere_mod4_eq_1(n):
    return n % 4 == 1

# Critère chaîne ≥ 3 avec '1' en antépénultième position
def critere_longueur_ge_3_antepenultieme_1(n):
    binaire = bin(n)[2:]
    return len(binaire) >= 3 and binaire[-3] == '1'
```

- La méthode affiche les premiers tests et vérifie que le résultat correspond au critère.

---

## Affichage des automates

- `Automate.afficher()` → transitions déterministes et états finaux.  
- `AutomateAFN.afficher()` → transitions multiples possibles pour chaque symbole.  
- `tableau_determinisation()` → tableau AFN → AFD, avec état puits si nécessaire.

## Remarques

- Les **AFN partiels** peuvent générer un **état puits** lors de la déterminisation.
- Chaque état AFD a désormais **une transition définie pour tous les symboles** de l’alphabet {0,1}.
- Les tests automatisés permettent de vérifier rapidement le comportement de l’automate sur un grand nombre d’entrées.

## Auteur

Romain Alves
