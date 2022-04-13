import json
import os
import unittest
from unittest.mock import patch

import questionnaire  # à partir de cet import je vais pouvoir appeler les classes et les méthodes de questionnaire
import questionnaire_import



def additionner(a, b):
    return a+b


class TestUnitaireDemo(unittest.TestCase):
    def test_additionner1(self):
        self.assertEqual(additionner(5, 10), 15)


class TestQuestion(unittest.TestCase):  # pour tester les questions
    def test_bonne_ou_mauvaise_reponse(self):  # grâce à cela on va pouvoir aller poser une question de façon simple
        q = questionnaire.Question("titre", ("choix1", "choix2", "choix3"), "choix3")
        with patch("builtins.input", return_value="1"):
            self.assertFalse(q.poser())  # on s'attend à ce que le retour de "poser la question" soit faux
        with patch("builtins.input", return_value="2"):
            self.assertFalse(q.poser())
        with patch("builtins.input", return_value="3"):
            self.assertTrue(q.poser())
        # ce que je rentre dans "return_valeur" correspond à ce que je pourrait rentrer au clavier directement
        # Ces tests devront être refait à chaque fois que l'on va effectuer des modifications dans le questionnaire par
        # exemple, afin de vérifier que le code en lui même n'a pas été cassé


class TestQuestionnaire(unittest.TestCase):  # on créé un nouvelle classe pour tester la création d'un questionnaire
    def test_questionnaire_lancer_cinema_starwars(self):
        filename = os.path.join("test_data", "cinema_starwars_confirme.json")
        q = questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNotNone(q)  # on vérifie qu'il n'est pas nul
        self.assertEqual(len(q.questions), 20)
        self.assertEqual(q.titre, "Star wars")
        self.assertEqual(q.categorie, "Cinéma")
        self.assertEqual(q.difficulte, "confirmé")
        #q.lancer()
        with patch("builtins.input", return_value="2"):  # permet de répondre 2 à toutes les questions
            self.assertEqual(q.lancer(), 5)  # permet de vérifier que le "score" est bien 5 (on veut recevoir "OK")
        # le nombre de question est dans l'objet "q". Tout cela est définit dans l'init du questionnaire

    def test_questionnaire_format_invalide(self):
        filename = os.path.join("test_data", "format_invalide1.json")
        q = questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNotNone(q)
        self.assertEqual(q.categorie, "inconnue")
        self.assertEqual(q.difficulte, "inconnue")
        self.assertIsNotNone(q.questions)

        filename = os.path.join("test_data", "format_invalide2.json")  # que les questions dans celui-ci
        q = questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNone(q)

        filename = os.path.join("test_data", "format_invalide3.json")
        q = questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNone(q)


class TestImportQuestionnaire(unittest.TestCase):  # surement le plus important
    def test_import_format_json(self):  # on va tester que le format de sortie est correct
        questionnaire_import.generate_json_file("Animaux",
                                                "Les chats",
                                                "https://www.kiwime.com/oqdb/files/1050288832/OpenQuizzDB_050/"
                                                "openquizzdb_50.json")
        # l'appel de cette fonction va générer 3 fichiers en sortie

        filenames = ("animaux_leschats_confirme.json", "animaux_leschats_debutant.json", "animaux_leschats_expert.json")
        for filename in filenames:
            self.assertTrue(os.path.isfile(filename))  # on va s'assurer que ce fichier existe
            file = open(filename)
            json_data = file.read()  # donné au format text
            file.close()
            try:
                data = json.loads(json_data)  # data au format structuré : on a désérialisé ici
            except:
                self.fail("ERREUR : problème de désérialisation" + filename)
            self.assertIsNotNone(data.get("titre"))
            self.assertIsNotNone(data.get("questions"))
            self.assertIsNotNone(data.get("difficulte"))
            self.assertIsNotNone(data.get("categorie"))

            # ensuite pour chaque question on va regarder que l'on a bien un titre
            for question in data.get("questions"):
                self.assertIsNotNone(question.get("titre"))
                self.assertIsNotNone(question.get("choix"))
                # jusqu'ici tout fonctionne, on va alors regarder ce qui se passe dans les choix
                for choix in question.get("choix"):  # on cherche à obtenir les choix dans "question"
                    self.assertGreater(len(choix[0]), 0)
                    # ceci équivaut à : "self.assertTrue(len(choix[0]) > 0)", mais le message serait - précis ici
                    self.assertTrue(isinstance(choix[1], bool))
            # cela va être une liste avec tous les éléments
                bonne_reponse = [i[0] for i in question.get("choix") if i[1]]  # donne la bonne réponse (on utilise "i", mais on aurait pu mettre n'importe quel élément ("choix" par exemple))
                self.assertEqual(len(bonne_reponse), 1)


            # ATTENTION
            # 'data["titre"]' : génére une exception si la clef n'existe pas / 'data.get["titre"]' : retourne un
            # 'None" si la clef n'existe pas


unittest.main()  # automatiquement il va reperer toutes les classes qui hérite de "unittest.TestCase" et il va exécuter
# toutes les méthodes qui commence par "test_"


# Remarque : avec tous les tests que l'on a encodé, si on venait à fournir notre code à un ou plusieurs développeur
# il pourrait faire plein de modifications dans tous les sens, mais la condition serait à chaque fois de relancer les
# tests et tant qu'il ne casse pas les tests on est confiant pour que le projet parte dans la bonne direction. Il ne
# faut pas tomber dans des test excessifs (en terme de temps passé). On reagrde ce qu'on appelle la courverture (cb de
# % de code on test)
