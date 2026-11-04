# Testeur d’automates binaires

[![Watch a one-minute video tour of testeur-d-automates-binaires](https://gitdiagram.com/video-badge.svg)](https://gitdiagram.com/4ppolyon/testeur-d-automates-binaires/video)

Un outil Python permettant de **modéliser, simuler, tester et visualiser des automates finis** :

- Automates finis déterministes (**AFD**)
- Automates finis non déterministes (**AFN**, avec ou sans ε-transitions)

L’alphabet utilisé est `{0,1}`.

---

## Fonctionnalités

Le projet permet :

- ✔️ de créer des **AFD et AFN**
- ✔️ de simuler la lecture de mots binaires
- ✔️ de tester automatiquement un automate avec un critère
- ✔️ de **déterminiser un AFN**
- ✔️ de **supprimer les ε-transitions**
- ✔️ de générer un **tableau de déterminisation**
- ✔️ de **dessiner les automates automatiquement (Graphviz)**

---

## Installation

### 1. Cloner le projet

```bash
git clone <repo_url>
cd <repo>
```

---
### 2. Installer les dépendances Python
```bash
pip install tqdm graphviz
```

---
### 3. Installer Graphviz (OBLIGATOIRE pour le dessin)

Télécharger ici : https://graphviz.org/download/

Version utilisée : `graphviz-14.1.3 (64-bit)` ⚠️ **Ajouter Graphviz au PATH** ⚠️

## Principe théorique

### Automate déterministe exemple : `n % 4 == 1`

Un entier est congruent à **1 modulo 4** si :  

- son écriture binaire se termine par `"01"`  
- ou il vaut `"1"`.  

L’automate implémenté exploite cette propriété et ne dépend que du **suffixe** du mot binaire.

| État | q0 (entrée 0) | q1 (entrée 1) | Final |
|------|---------------|---------------|-------|
| e0   | e0            | e1            | ❌    |
| e1   | e0            | e2            | ✅    |
| e2   | e0            | e2            | ❌    |

---

### Automate non déterministe exemple : détection d’un 1 en antépénultième position

**Automate non déterministe** désigne un type d’automate où, pour un même état et un même symbole d’entrée, il peut y
avoir **plusieurs transitions possibles** vers différents états. Dans notre exemple, l’automate reconnaît toutes les
chaînes de longueur ≥ 3 ayant un `'1'` en **antépénultième position**.

| État | 0 | 1 | Final |
|------|---|---|-------|
| e0   | {e0} | {e0, e1} | ❌ |
| e1   | {e2} | {e2} | ❌ |
| e2   | {e3} | {e3} | ❌ |
| e3   | {}   | {}   | ✅ |

---

### ε-transitions

Transitions sans consommation de symbole (asynchrone) :
- Éliminée par la methode des ε-clôtures
- Doivent être supprimées avant déterminisation
- Exemple sur l’automate non déterministe précédent :
```
TEST DE L'AUTOMATE NON DÉTERMINISTE AVEC ε-TRANSITIONS RECONNAISSANT LES NOMBRES DONT LA
REPRÉSENTATION BINAIRE CONTIENT UNE SUITE ALTERNANTE DE '0' ET '1'

Automate AFN:
État e0: 0 -> {}, 1 -> {}, ε -> {e1, e2}
État e1 (final): 0 -> {e2}, 1 -> {}, ε -> {}
État e2 (final): 0 -> {}, 1 -> {e1}, ε -> {}


SUPPRESSION DES ε-TRANSITIONS

ε-clôture(e0) : {e1,e0,e2}
ε-clôture(e1) : {e1}
ε-clôture(e2) : {e2}

Traitement de l’état e0
  Symbole 0 :
    depuis e1 vers la cloture de e2, qui est {e2}
    depuis e0
    depuis e2
    → {{e2}}
  Symbole 1 :
    depuis e1
    depuis e0
    depuis e2 vers la cloture de e1, qui est {e1}
    → {{e1}}

Traitement de l’état e1
  Symbole 0 :
    depuis e1 vers la cloture de e2, qui est {e2}
    → {{e2}}
  Symbole 1 :
    depuis e1
    → {}

Traitement de l’état e2
  Symbole 0 :
    depuis e2
    → {}
  Symbole 1 :
    depuis e2 vers la cloture de e1, qui est {e1}
    → {{e1}}

✔ {e1,e0,e2} devient FINAL
✔ {e1} devient FINAL
✔ {e2} devient FINAL

Automate AFN:
État {e1,e0,e2} (final): 0 -> {{e2}}, 1 -> {{e1}}, ε -> {}
État {e1} (final): 0 -> {{e2}}, 1 -> {}, ε -> {}
État {e2} (final): 0 -> {}, 1 -> {{e1}}, ε -> {}
```

---
### Déterminisation

Nous avons fait le choix de transformer un **AFN** en **AFD Complet**.

C'est-à-dire que :
- Si certaines transitions "*n’existent pas*", un **état puits** est créé et l’AFD résultant a une transition pour **tous les symboles de chaque état**.

---

### Tests automatisés

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

### Affichage des automates

- `Automate.afficher()` → transitions déterministes et états finaux.  
- `Automate.dessiner("nom_fichier")` → dessin de l’automate avec Graphviz et sauvegarde au format PNG.
  - état initial → flèche entrante 
  - état final → double cercle 
  - transitions étiquetées (0, 1)
  - Les fichiers sont générés en .png
- `AutomateAFN.afficher()` → transitions multiples possibles pour chaque symbole.
- `AutomateAFN.dessiner("nom_fichier")` → dessin de l’AFN avec Graphviz et sauvegarde au format PNG. 
  - état initial → flèche entrante 
  - état final → double cercle 
  - transitions étiquetées (0, 1, ε)
  - Les fichiers sont générés en .png
- `tableau_determinisation()` → tableau AFN → AFD, avec état puits si nécessaire.

---

## Structure du code
Classes principales :
- `Etat` → état d’un AFD
- `EtatAFN` → état d’un AFN (avec transitions multiples + ε)
- `Automate` → AFD
- `AutomateAFN` → AFN
- `TestAutomate` → moteur de tests

---

## Fonctionnalités avancées
- `epsilon_cloture()` → calcule la fermeture ε
- `supprimer_epsilon()` → transforme AFN ε → AFN standard
- `tableau_determinisation()` → affichage pédagogique
- `determiniser()` → AFN → AFD

---

## Exemples inclus

- AFD → modulo 4
- AFN → antépénultième = 1
- AFN avec ε → alternance 0/1
- AFN complexe → se termine par 011

---

## Problèmes courants
```❌ Erreur : dot not found```

Solution :

1. Installer Graphviz (si ce n’est pas déjà fait : https://graphviz.org/download/)
2. Ajouter au PATH (sur windows une option est de cocher "Add Graphviz to the system PATH" lors de l’installation)
3. Redémarrer le terminal

---

## Remarques

- Les tests automatisés permettent de vérifier rapidement le comportement de l’automate sur un grand nombre d’entrées.
- La visualisation avec Graphviz facilite la compréhension de la structure de l’automate et de ses transitions.
- Ce projet est à but pédagogique (uniquement), pour illustrer les concepts d’automates finis déterministes et non déterministes, ainsi que les transformations entre eux.
- Le projet est réalisé en Python
- Le projet est réalisé sur mon temps libre, sans contrainte de délai et en parallele de ma thèse de doctorat, il est donc possible que certaines fonctionnalités soient incomplètes ou que des bugs subsistent, n’hésitez pas à me contacter pour toute question ou suggestion d’amélioration.

## Auteur

Romain Alves
- [GitHub](https://github.com/4ppolyon)
- [LinkedIn](https://www.linkedin.com/in/romainalves/)
- [Email](mailto:romalves@lisn.fr)
