import time
from tqdm import tqdm

class Etat:
    def __init__(self, nom, q0=None, q1=None, final=False):
        self.nom = nom
        self.q0 = q0  # références directes à d'autres objets Etat
        self.q1 = q1
        self.final = final

    def est_final(self):
        return self.final

    def transition(self, symbole):
        if symbole == '0':
            return self.q0
        elif symbole == '1':
            return self.q1
        else:
            raise ValueError(f"Entrée invalide : {symbole}. Doit être '0' ou '1'.")

class EtatAFN:
    def __init__(self, nom, final=False):
        self.nom = nom
        self.transitions = {
            '0': set(),
            '1': set(),
            'ε': set()
        }
        self.final = final

    def ajouter_transition(self, symbole, etat):
        self.transitions[symbole].add(etat)

    def est_final(self):
        return self.final


class Automate:
    def __init__(self, etats, etat_initial):
        self.etats = etats
        self.etat_initial = etat_initial
        self.etat_courant = etat_initial

    def afficher(self):
        print("Automate:")
        for etat in self.etats:
            final_str = " (final)" if etat.est_final() else ""
            print(f"État {etat.nom}{final_str}: 0 -> {etat.q0.nom}, 1 -> {etat.q1.nom}")
        print()

    def lire_chaine(self, chaine):
        self.etat_courant = self.etat_initial
        etats_visites = [self.etat_courant.nom]

        for symbole in chaine:
            self.etat_courant = self.etat_courant.transition(symbole)
            etats_visites.append(self.etat_courant.nom)

        return self.etat_courant.est_final(), etats_visites
    

class AutomateAFN:
    def __init__(self, etats, etat_initial):
        self.etats = etats
        self.etat_initial = etat_initial
    
    def afficher(self):
        print("Automate AFN:")
        for etat in self.etats:
            final_str = " (final)" if etat.est_final() else ""
            t0 = ", ".join(e.nom for e in etat.transitions['0'])
            t1 = ", ".join(e.nom for e in etat.transitions['1'])
            print(f"État {etat.nom}{final_str}: 0 -> {{{t0}}}, 1 -> {{{t1}}}")
        print()

    def epsilon_cloture(self, etat):
        pile = [etat]
        cloture = {etat}

        print(f"ε-clôture({etat.nom}) : ", end="")

        while pile:
            courant = pile.pop()
            for e in courant.transitions['ε']:
                if e not in cloture:
                    cloture.add(e)
                    pile.append(e)
        nom_cloture = "{" + ",".join(e.nom for e in cloture) + "}"
        print(nom_cloture)
        return cloture, nom_cloture

    def supprimer_epsilon(self):

        nouveaux_etats = {}

        # Étape 1 : ε-clôtures
        clotures = {}
        for e in self.etats:
            combinaison, nom_cloture = self.epsilon_cloture(e)
            clotures[e] = {"nom" : nom_cloture, "etats": combinaison}
            if nom_cloture not in nouveaux_etats:
                nouveaux_etats[nom_cloture] = EtatAFN(nom=nom_cloture)

        # Étape 2 : nouvelles transitions (sans ε)
        for e in self.etats:
            print(f"\nTraitement de l’état {e.nom}")

            for symbole in ['0', '1']:
                destination = []

                print(f"  Symbole {symbole} :")

                for p in clotures[e]["etats"]:
                    print(f"    depuis {p.nom}", end="")
                    for q in p.transitions[symbole]:
                        # ajouter la ε-clôture de q à la destination
                        print(f" vers la cloture de {q.nom}, qui est {clotures[q]["nom"]}", end="")
                        destination.append(q)
                    print()

                for d in destination:
                    nouveaux_etats[clotures[e]["nom"]].ajouter_transition(symbole, nouveaux_etats[clotures[d]["nom"]])

                print("    → {" + ",".join(nouveaux_etats[clotures[d]["nom"]].nom for d in destination) + "}")
        print()

        # Étape 3 : états finaux
        for e in self.etats:
            if any(p.est_final() for p in clotures[e]["etats"]):
                nouveaux_etats[clotures[e]["nom"]].final = True
                print(f"✔ {clotures[e]["nom"]} devient FINAL")
        print()

        return AutomateAFN(
            etats=list(nouveaux_etats[clotures[e]["nom"]] for e in self.etats),
            etat_initial=nouveaux_etats[clotures[self.etat_initial]["nom"]]
        )

    def tableau_determinisation(self):
        symboles = ['0', '1']

        # chaque état de l’AFD est un ensemble d’états de l’AFN
        etat_initial = frozenset([self.etat_initial])
        a_traiter = [etat_initial]
        deja_vus = set(a_traiter)

        print("\nTABLEAU DE DÉTERMINISATION (AFN → AFD)\n")
        print(f"{'État AFN':^20} | {'0':^20} | {'1':^20} | {'Final':^7}")
        print("-" * 75)

        while a_traiter:
            etat_courant = a_traiter.pop(0)

            transitions = {}
            est_final = any(e.est_final() for e in etat_courant)

            for symbole in symboles:
                nouvel_etat = set()
                for e in etat_courant:
                    nouvel_etat |= e.transitions[symbole]

                nouvel_etat = frozenset(nouvel_etat)
                transitions[symbole] = nouvel_etat

                if nouvel_etat not in deja_vus:
                    deja_vus.add(nouvel_etat)
                    a_traiter.append(nouvel_etat)

            nom_etat = "{" + ",".join(e.nom for e in etat_courant) + "}"
            t0 = "{" + ",".join(e.nom for e in transitions['0']) + "}"
            t1 = "{" + ",".join(e.nom for e in transitions['1']) + "}"

            print(f"{nom_etat:^20} | {t0:^20} | {t1:^20} | {'✅' if est_final else '❌':^7}")
        print()
    
    def determiniser(self):
        symboles = ['0', '1']

        # État initial de l’AFD = ensemble contenant l’état initial AFN
        etat_initial_afn = frozenset([self.etat_initial])

        # dictionnaire : ensemble AFN -> Etat AFD
        mapping = {}

        # file BFS
        a_traiter = [etat_initial_afn]

        # création de l’état initial AFD
        nom_init = "{" + ",".join(e.nom for e in etat_initial_afn) + "}"
        etat_init_afd = Etat(
            nom=nom_init,
            final=any(e.est_final() for e in etat_initial_afn)
        )

        mapping[etat_initial_afn] = etat_init_afd

        while a_traiter:
            etat_courant_afn = a_traiter.pop(0)
            etat_courant_afd = mapping[etat_courant_afn]

            for symbole in symboles:
                nouvel_etat_afn = set()

                for e in etat_courant_afn:
                    nouvel_etat_afn |= e.transitions[symbole]

                nouvel_etat_afn = frozenset(nouvel_etat_afn)

                if nouvel_etat_afn not in mapping:
                    nom = "{" + ",".join(e.nom for e in nouvel_etat_afn) + "}"
                    mapping[nouvel_etat_afn] = Etat(
                        nom=nom,
                        final=any(e.est_final() for e in nouvel_etat_afn)
                    )
                    a_traiter.append(nouvel_etat_afn)

                # connexion des transitions AFD
                if symbole == '0':
                    etat_courant_afd.q0 = mapping[nouvel_etat_afn]
                else:
                    etat_courant_afd.q1 = mapping[nouvel_etat_afn]

        # Automate déterministe final
        return Automate(
            etats=list(mapping.values()),
            etat_initial=etat_init_afd
        )
        

class TestAutomate:
    def __init__(self, automate):
        self.automate = automate

    def tester_automate(self, critere, n_tests=1_000_000, afficher_premiers=10):
        print(f"Début des tests pour {n_tests} nombres...")
        start_time = time.time()

        """
        critere : fonction prenant un entier i et renvoyant True / False
        """

        premiers_tests = []

        for i in tqdm(range(n_tests), desc="Tests en cours", unit="test"):
            binaire = bin(i)[2:]  # conversion en binaire sans le préfixe '0b'
            attendu = critere(i)
            resultat, etats_visites = self.automate.lire_chaine(binaire)

            if i < afficher_premiers:
                premiers_tests.append((binaire, attendu, resultat, etats_visites))

            assert resultat == attendu, (
                f"Erreur pour {binaire} ({i}): attendu {attendu}, obtenu {resultat}\n"
                f"États visités: {' -> '.join(etats_visites)}"
            )

        end_time = time.time()

        print(f"\nPremiers {afficher_premiers} tests :")
        for binaire, attendu, resultat, etats_visites in premiers_tests:
            print(f"Chaîne: {binaire}, attendu: {'✅' if attendu else '❌'}, obtenu: {'✅' if resultat else '❌'}, "
                  f"États: {' -> '.join(etats_visites)}")
        print(f"\n✅ Tous les tests passés en {end_time - start_time:.2f} secondes.\n")


if __name__ == "__main__":

    print("\nTESTS DE L'AUTOMATE BINAIRE RECONNAISSANT LES NOMBRES ≡ 1 (mod 4)\n")

    # Création des états pour l'automate déterministe
    e0 = Etat("e0")
    e1 = Etat("e1", final=True)
    e2 = Etat("e2")

    # Définition des transitions pour l'automate déterministe
    e0.q0, e0.q1 = e0, e1
    e1.q0, e1.q1 = e0, e2
    e2.q0, e2.q1 = e0, e2

    automate = Automate([e0, e1, e2], e0)
    automate.afficher()

    print("\nTESTS DE L'AUTOMATE DÉTERMINISTE\n")

    test = TestAutomate(automate=automate)
    def critere_mod4_eq_1(n):
        return n % 4 == 1
    test.tester_automate(critere=critere_mod4_eq_1, n_tests=100000, afficher_premiers=10)

    print("_"*180 +"\n\nTEST DE LA DÉTERMINISATION D'UN AFN RECONNAISSANT LES CHAÎNES DE LONGUEUR ≥ 3\n"
                  "AVEC UN '1' EN ANTÉPÉNULTIME CARACTÈRE\n")

    # Création des états pour l'automate non déterministe
    e0 = EtatAFN("e0")
    e1 = EtatAFN("e1")
    e2 = EtatAFN("e2")
    e3 = EtatAFN("e3", final=True)

    # Définition des transitions pour l'automate non déterministe
    e0.ajouter_transition('0', e0)
    e0.ajouter_transition('1', e0)
    e0.ajouter_transition('1', e1)
    e1.ajouter_transition('0', e2)
    e1.ajouter_transition('1', e2)
    e2.ajouter_transition('0', e3)
    e2.ajouter_transition('1', e3)

    afn = AutomateAFN([e0, e1, e2, e3], e0)
    afn.afficher()

    print("\nDÉTERMINISATION DE L'AFN\n")

    afn.tableau_determinisation()
    afd = afn.determiniser()
    afd.afficher()

    print("\nTESTS DE L'AUTOMATE DÉTERMINISTE OBTENU APRÈS DÉTERMINISATION\n")

    test_afd = TestAutomate(automate=afd)
    def critere_longueur_ge_3_antepenultieme_1(n):
        binaire = bin(n)[2:] # conversion en binaire sans le préfixe '0b'
        return len(binaire) >= 3 and binaire[-3] == '1'
    test_afd.tester_automate(critere=critere_longueur_ge_3_antepenultieme_1, n_tests=100000, afficher_premiers=10)

    print("_"*180 +"\n\nTEST DE L'AUTOMATE NON DÉTERMINISTE AVEC ε-TRANSITIONS RECONNAISSANT LES NOMBRES DONT LA\n"
                  "REPRÉSENTATION BINAIRE CONTIENT UNE SUITE ALTERNANTE DE '0' ET '1'\n")

    # Création des états pour l'automate non déterministe avec ε-transitions
    e0 = EtatAFN("e0")
    e1 = EtatAFN("e1", final=True)
    e2 = EtatAFN("e2", final=True)

    # Définition des transitions pour l'automate non déterministe avec ε-transitions
    e0.ajouter_transition('ε', e1)
    e0.ajouter_transition('ε', e2)
    e1.ajouter_transition('0', e2)
    e2.ajouter_transition('1', e1)

    afn_epsilon = AutomateAFN([e0, e1, e2], e0)
    afn_epsilon.afficher()

    print("\nSUPPRESSION DES ε-TRANSITIONS\n")

    afn_sans_epsilon = afn_epsilon.supprimer_epsilon()
    afn_sans_epsilon.afficher()

    print("\nDÉTERMINISATION DE L'AFN SANS ε-TRANSITIONS\n")

    afn_sans_epsilon.tableau_determinisation()
    afd_final = afn_sans_epsilon.determiniser()
    afd_final.afficher()

    print("\nTESTS DE L'AUTOMATE DÉTERMINISTE OBTENU APRÈS DÉTERMINISATION ET SUPPRESSION DES ε-TRANSITIONS\n")

    test_afd_final = TestAutomate(automate=afd_final)
    def critere_alternance_01(n):
        binaire = bin(n)[2:] # conversion en binaire sans le préfixe '0b'
        return all(binaire[i] != binaire[i+1] for i in range(len(binaire)-1))
    test_afd_final.tester_automate(critere=critere_alternance_01, n_tests=100000, afficher_premiers=10)

    print("_"*180 +"\n\nTEST DE L'AUTOMATE NON DÉTERMINISTE AVEC ε-TRANSITIONS RECONNAISSANT LES NOMBRES DONT LA\n"
                  "REPRÉSENTATION BINAIRE SE TERMINE PAR '011'\n")

    # Création des états pour l'automate non déterministe avec ε-transitions
    e0 = EtatAFN("0")
    e1 = EtatAFN("1")
    e2 = EtatAFN("2")
    e3 = EtatAFN("3")
    e4 = EtatAFN("4")
    e5 = EtatAFN("5")
    e6 = EtatAFN("6")
    e7 = EtatAFN("7")
    e8 = EtatAFN("8")
    e9 = EtatAFN("9")
    e10 = EtatAFN("10", final=True)

    # Définition des transitions pour l'automate non déterministe avec ε-transitions
    e0.ajouter_transition('ε', e1)
    e0.ajouter_transition('ε', e6)
    e1.ajouter_transition('ε', e2)
    e2.ajouter_transition('0', e3)
    e3.ajouter_transition('ε', e6)
    e1.ajouter_transition('ε', e4)
    e4.ajouter_transition('1', e5)
    e5.ajouter_transition('ε', e6)
    e6.ajouter_transition('ε', e1)
    e6.ajouter_transition('ε', e7)
    e7.ajouter_transition('0', e8)
    e8.ajouter_transition('1', e9)
    e9.ajouter_transition('1', e10)

    afn_epsilon = AutomateAFN([e0, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10], e0)
    afn_epsilon.afficher()

    print("\nSUPPRESSION DES ε-TRANSITIONS\n")

    afn_sans_epsilon = afn_epsilon.supprimer_epsilon()
    afn_sans_epsilon.afficher()

    print("\nDÉTERMINISATION DE L'AFN SANS ε-TRANSITIONS\n")

    afn_sans_epsilon.tableau_determinisation()
    afd_final = afn_sans_epsilon.determiniser()
    afd_final.afficher()

    print("\nTESTS DE L'AUTOMATE DÉTERMINISTE OBTENU APRÈS DÉTERMINISATION ET SUPPRESSION DES ε-TRANSITIONS\n")

    test_afd_final = TestAutomate(automate=afd_final)
    def critere_fini_par_abb(n):
        binaire = bin(n)[2:] # conversion en binaire sans le préfixe '0b'
        return binaire.endswith('011')
    test_afd_final.tester_automate(critere=critere_fini_par_abb, n_tests=100000, afficher_premiers=20)
