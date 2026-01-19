class etat:
    def __init__(self, nom, q0, q1, final=False):
        self.nom = nom
        self.q0 = q0
        self.q1 = q1
        self.final = final

    def afficher(self):
        return f"État: {self.nom}, q0: {self.q0}, q1: {self.q1}, final: {self.final}"
    
    def est_final(self):
        return self.final
    
    def transition(self, entree):
        if entree == '0':
            return self.q0
        elif entree == '1':
            return self.q1
        else:
            raise ValueError("Entrée invalide, doit être '0' ou '1'")
    
class automate:
    def __init__(self, etats, etat_initial):
        self.etats = {etat.nom: etat for etat in etats}
        self.etat_initial = etat_initial
        self.etat_courant = self.etats[etat_initial]

    def lire_chaine(self, chaine):
        self.etat_courant = self.etats[self.etat_initial]  # Réinitialiser à l'état initial
        etats_visites = [self.etat_courant.nom]
        for symbole in chaine:
            self.etat_courant = self.etats[self.etat_courant.transition(symbole)]
            etats_visites.append(self.etat_courant.nom)
        return self.etat_courant.est_final(), etats_visites
    
class test_automate_bin:
    def __init__(self):
        
        e0 = etat("e0", "e0", "e1", final=False)
        e1 = etat("e1", "e0", "e2", final=True)
        e2 = etat("e2", "e0", "e2", final=False)
        self.automate = automate([e0, e1, e2], "e0")
    
    def translate_to_binary(self, n):
        # print("Traduction de",n,"en binaire :",end=" ")
        if n == 0:
            # print("0")
            return "0"
        bits = []
        while n > 0:
            bits.append(str(n % 2))
            n //= 2
        bits_str = ''.join(reversed(bits))
        # print(bits_str)
        return bits_str

    def tester(self):

        def afficher_premiers_tests(tests, n=10):
            print("Premiers tests générés :")
            for i, (chaine, attendu) in enumerate(tests.items()):
                if i >= n:
                    break
                print(f"Chaîne: {chaine}, Attendu: {'✅' if attendu else '❌'}")

        tests = {}
        for i in range(4096):
            binaire = self.translate_to_binary(i)
            tests[binaire] = (i % 4 == 1)
        
        afficher_premiers_tests(tests)

        print("Début des tests...")
        start_time = __import__('time').time()
        for chaine, attendu in tests.items():
            resultat, etats_visites = self.automate.lire_chaine(chaine)
            # print(f"Chaîne: {chaine}, États visités: {etats_visites}, Résultat: {'✅' if resultat else '❌'}")
            assert resultat == attendu, f"Échec pour la chaîne '{chaine}': attendu {attendu}, obtenu {resultat}"
        end_time = __import__('time').time()
        print(f"Tous les tests sont passés avec succès. ✅ Temps écoulé: {end_time - start_time:.2f} secondes")

if __name__ == "__main__":
    test = test_automate_bin()
    # test.translate_to_binary(25)
    test.tester()
