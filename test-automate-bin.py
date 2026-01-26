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


class TestAutomateBin:
    def __init__(self):
        # Création des états
        e0 = Etat("e0", final=False)
        e1 = Etat("e1", final=True)
        e2 = Etat("e2", final=False)

        # Définition des transitions
        e0.q0, e0.q1 = e0, e1
        e1.q0, e1.q1 = e0, e2
        e2.q0, e2.q1 = e0, e2

        # Automate
        self.automate = Automate([e0, e1, e2], e0)

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
    test = TestAutomateBin()
    test.tester(n_tests=1000000, afficher_premiers=10)
