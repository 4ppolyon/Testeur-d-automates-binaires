# Testeur-d-automates-binaires

Un outil Python permettant de **modéliser, simuler et tester des automates finis déterministes (AFD)** sur l’alphabet binaire `{0,1}`.  
Le projet vérifie automatiquement qu’un automate reconnaît correctement un langage binaire donné.

Dans la version actuelle, l’automate testé reconnaît les entiers **congruents à 1 modulo 4**, codés en binaire et lus de gauche à droite (bit de poids fort en premier).

---

## Objectif

- Implémenter un **automate fini déterministe**
- Simuler la lecture de mots binaires
- Tester automatiquement un automate sur un grand nombre d’entrées
- Vérifier la correspondance entre :
  
\[
L = \{ n \in \mathbb{N} \mid n \equiv 1 \pmod{4} \}
\]

et le comportement de l’automate

---

## Principe théorique

Un entier est congruent à **1 modulo 4** si et seulement si :
- son écriture binaire est `"1"`, ou
- elle se termine par `"01"`

L’automate implémenté exploite cette propriété et ne dépend que du **suffixe** du mot binaire.

---

### Auteur
- Romain Alves

