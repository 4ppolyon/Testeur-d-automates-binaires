import time

class Etat:
    def __init__(self, nom, q0=None, q1=None, final=False):
        self.nom = nom
        self.q0 = q0  # références directes à d'autres objets Etat
        self.q1 = q1
        self.final = final

    def __str__(self):
        return f"{self.nom} (final={self.final})"

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

    def __str__(self):
        return self.nom


class Automate:
    def __init__(self, etats, etat_initial):
        self.etats = etats
        self.etat_initial = etat_initial
        self.etat_courant = etat_initial

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

class TestAutomateBin:
    def __init__(self, automate):
        self.automate = automate

    @staticmethod
    def translate_to_binary(n):
        return bin(n)[2:]

    def tester(self, n_tests=1_000_000, afficher_premiers=10):
        print(f"Début des tests pour {n_tests} nombres...")
        start_time = time.time()

        premiers_tests = []

        for i in range(n_tests):
            binaire = self.translate_to_binary(i)
            attendu = (i % 4 == 1)
            resultat, etats_visites = self.automate.lire_chaine(binaire)

            if i < afficher_premiers:
                premiers_tests.append((binaire, attendu, resultat, etats_visites))

            assert resultat == attendu, (
                f"Erreur pour {binaire} ({i}): attendu {attendu}, obtenu {resultat}\n"
                f"États visités: {' -> '.join(etats_visites)}"
            )

        end_time = time.time()
        print(f"✅ Tous les tests passés en {end_time - start_time:.2f} secondes.\n")

        print(f"Premiers {afficher_premiers} tests :")
        for binaire, attendu, resultat, etats_visites in premiers_tests:
            print(f"Chaîne: {binaire}, attendu: {'✅' if attendu else '❌'}, obtenu: {'✅' if resultat else '❌'}, "
                  f"États: {' -> '.join(etats_visites)}")


if __name__ == "__main__":

    print("\nTESTS DE L'AUTOMATE BINAIRE RECONNAISSANT LES NOMBRES ≡ 1 (mod 4)\n")
    # Création des états
    e0 = Etat("e0")
    e1 = Etat("e1", final=True)
    e2 = Etat("e2")

    # Définition des transitions
    e0.q0, e0.q1 = e0, e1
    e1.q0, e1.q1 = e0, e2
    e2.q0, e2.q1 = e0, e2

    automate = Automate([e0, e1, e2], e0)

    test = TestAutomateBin(automate=automate)
    test.tester(n_tests=1000000, afficher_premiers=10)

    print("\nTEST DE LA DÉTERMINISATION D'UN AFN RECONNAISSANT LES CHAÎNES DE LONGUEUR ≥ 3 "
          "AVEC UN '1' EN ANTÉPÉNULTIME CARACTÈRE\n")

    # Création des états pour le tableau de déterminisation
    e0 = EtatAFN("e0")
    e1 = EtatAFN("B")
    e2 = EtatAFN("e2")
    e3 = EtatAFN("e3", final=True)

    # Définition des transitions pour le tableau de déterminisation
    e0.ajouter_transition('0', e0)
    e0.ajouter_transition('1', e0)
    e0.ajouter_transition('1', e1)
    e1.ajouter_transition('0', e2)
    e1.ajouter_transition('1', e2)
    e2.ajouter_transition('0', e3)
    e2.ajouter_transition('1', e3)

    afn = AutomateAFN([e0, e1, e2, e3], e0)

    afn.tableau_determinisation()