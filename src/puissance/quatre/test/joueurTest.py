from src.puissance.quatre.model.joueur import Joueur

import unittest

class TestJoueur(unittest.TestCase):

    def test_setNom(self):
        joueur = Joueur("John")
        joueur.setNom("Doe")
        self.assertEqual(joueur.getNom(), "Doe")

    def test_setNom_exception(self):
        joueur = Joueur("Alice")
        with self.assertRaises(ValueError):
            joueur.setNom("")

    def test_getNom(self):
        joueur = Joueur("Alice")
        self.assertEqual(joueur.getNom(), "Alice")

    def test_init(self):
        joueur = Joueur("Bob")
        self.assertEqual(joueur.getNom(), "Bob")

if __name__ == '__main__':
    unittest.main()
