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
            '1': set()
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

    test = TestAutomate(automate=automate)

    def critere_mod4_eq_1(n):
        return n % 4 == 1
    
    test.tester_automate(critere=critere_mod4_eq_1, n_tests=1000000, afficher_premiers=10)

    print("_"*80 +"\n\nTEST DE LA DÉTERMINISATION D'UN AFN RECONNAISSANT LES CHAÎNES DE LONGUEUR ≥ 3\n"
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

    afn.tableau_determinisation()
    afd = afn.determiniser()
    afd.afficher()

    print("_"*80 +"\n\nTESTS DE L'AUTOMATE DÉTERMINISTE OBTENU APRÈS DÉTERMINISATION\n")
    test_afd = TestAutomate(automate=afd)

    def critere_longueur_ge_3_antepenultieme_1(n):
        binaire = bin(n)[2:] # conversion en binaire sans le préfixe '0b'
        return len(binaire) >= 3 and binaire[-3] == '1'

    test_afd.tester_automate(critere=critere_longueur_ge_3_antepenultieme_1, n_tests=1000000, afficher_premiers=10)