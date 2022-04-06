import json

# PROJET QUESTIONNAIRE V3 : POO
#
# - Pratiquer sur la POO
# - Travailler sur du code existant
# - Mener un raisonnement
#
# -> Définir les entitées (données, actions)
#
# Question
#    - titre       - str
#    - choix       - (str)
#    - bonne_reponse   - str
#
#    - poser()  -> bool
#
# Questionnaire
#    - questions      - (Question)
#
#    - lancer()
#


# dans ce questionnaire l'iéde est que : au lien d'utiliser des données en dur comme c'est le cas acutellement,
# on va charger un fichier "json" récupéré dans le fichier "import" le désérialiser et l'utiliser. Au débu on lui passera le fichier en dur,
# puis on rajoutera la possiblité de lui passer le fichier en ligne de commande


class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def FromData(data):
        # ....
        q = Question(data[2], data[0], data[1])
        return q

    def poser(self):  # cette fonction est appelé à chaque nouvelle question
        # print("QUESTION")
        print("  " + self.titre)
        for i in range(len(self.choix)):
            print("  ", i + 1, "-", self.choix[i])

        print()
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_numerique_utlisateur(1, len(self.choix))
        if self.choix[reponse_int - 1].lower() == self.bonne_reponse.lower():
            print("Bonne réponse")
            resultat_response_correcte = True
        else:
            print("Mauvaise réponse")

        print()
        return resultat_response_correcte

    def demander_reponse_numerique_utlisateur(min, max):
        reponse_str = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") : ")
        try:
            reponse_int = int(reponse_str)
            if min <= reponse_int <= max:
                return reponse_int

            print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.demander_reponse_numerique_utlisateur(min, max)


class Questionnaire:
    numero_question = 0

    def __init__(self, questions):
        self.questions = questions

    def lancer(self):
        print("CATEGORIE : " + categorie)
        print()
        print("TITRE : " + titre)
        print()
        #  print(len(self.questions))
        score = 0
        for question in self.questions:
            self.numero_question += 1
            print("QUESTION N°" + str(self.numero_question) + " / " + str(
                len(self.questions)))  # on met ce "print" ici pour avoir le numéro de la question
            if question.poser():
                score += 1
        print("Score final :", score, "sur", len(self.questions))
        return score


"""questionnaire = (
    ("Quelle est la capitale de la France ?", ("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris"), 
    ("Quelle est la capitale de l'Italie ?", ("Rome", "Venise", "Pise", "Florence"), "Rome"),
    ("Quelle est la capitale de la Belgique ?", ("Anvers", "Bruxelles", "Bruges", "Liège"), "Bruxelles")
                )

lancer_questionnaire(questionnaire)"""

# q1 = Question("Quelle est la capitale de la France ?", ("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris")
# q1.poser()

# data = (("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris", "Quelle est la capitale de la France ?")
# q = Question.FromData(data)
# print(q.__dict__)

# Questionnaire(
#   (
#  Question("Quelle est la capitale de la France ?", ("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris"),
# Question("Quelle est la capitale de l'Italie ?", ("Rome", "Venise", "Pise", "Florence"), "Rome")
# Question("Quelle est la capitale de la Belgique ?", ("Anvers", "Bruxelles", "Bruges", "Liège"), "Bruxelles")
# )
# ).lancer()


# ce que l'on  obtient à la suite du "import" sur le chat par ex
#  [
#  {   'titre': "À quelle classe d'animaux vertébrés regroupant près de 5.400 espèces appartient le chat ?",
# 'choix': [('Oiseaux', False), ('Poissons', False), ('Mammifères', True), ('Reptiles', False)]   },
#  {'titre': 'Lorsque vous apercevez votrchat faire le gros dos, il est probablement...',
#  'choix': [('Malade', False), ('En chasse', False), ('Effrayé', True), ('Content', False)]}

# Ceci est sous forme d'un dico

# On va charger un fichier json, désérilaiser les données et faire tourner le qestionnaire à partir des données qui
# sont dans un fichier. C'est à dire que l'on va récupérer des données texte et on va les mettre sous forme d'un dico


# Questionnaire(
#   (
#  Question(questions[1]['titre'], (questions[1]['choix'][0][0], questions[1]['choix'][1][0], questions[1]['choix'][2][0], questions[1]['choix'][3][0]), questions[1]['choix'][2][0]),
# Question(questions[2]['titre'], (questions[2]['choix'][0][0], questions[2]['choix'][1][0], questions[2]['choix'][2][0], questions[2]['choix'][3][0]), questions[2]['choix'][2][0]),
# Question("Quelle est la capitale de l'Italie ?", ("Rome", "Venise", "Pise", "Florence"), "Rome")
# )).lancer()
# lancer le questionnaire n'a pour but que de lancer toutes les questions les unes à la suite des autres


# NOUVEAU TRAVAIL / les fichiers "json" que l'on récupère sont au format texte
f = open("cinema_starwars_confirme.json", "r")  # on ouvre le fichier json avec toutes les questions et réponse
f_reading = f.read()  # on créé un fichier de lecture
f_reading_dico = json.loads(f_reading)  # on désérialise : "texte -> dico". C'est un dictionnaire dans lequel on a
# toutes les questions (on aura pu le faire après le "close" si on le souhaitais)
#   print(f_reading_dico)
f.close()  # on a tout copier dans le dico "f_reading_dico" on peut fermer le fichier texte


# on récupère les données du dico 
questions = f_reading_dico["questions"]  # toutes les questions du dictionnaire
categorie = f_reading_dico["categorie"]  # la catégorie du quizz
titre = f_reading_dico["titre"]  # la titre du quizz
#   print(questions)
#   print(categorie)
#   print(titre)

#   print(questions[1]['titre'])  # question 2
#   print(questions[3]['choix'])  # tous les choix choix de la question 4
#   print(questions[5]['choix'][0][0])  # Choix 1 de la question 6
#   print(questions[5]['choix'][2][0])  # Choix 3 de la question 6

Question_list = []
#   print(questions)
#   print(len(questions))
for i in range(0, len(questions)):  # le nombre de question est : "len(questions)"
    # pour chacune des questions on veut définir quelle est la bonne réponse
    Bonne_rep = None  # on initialise ce paramètre pour chacune des questions
    print(Bonne_rep)
    print("i : " + str(i))
    print("les choix de reponse pour la question " + str(i+1) + " sont : " + str(questions[i]['choix']))  # correspond
    # à la liste des "[]" qui représente les choix et un booléean
    for j in range(0, len(questions[i]['choix'])):
        #   print("j :" + str(j))
        #   print(questions[i]['choix'][j][1])
        if questions[i]['choix'][j][1]:  # si on rencontre le "True" on retient le numéro dans les différentes réponses
            print("la place du True dans les réponse est : " + str(j+1))
            Bonne_rep = questions[i]['choix'][j][0]
            print("la bonne réponse associée est : " + Bonne_rep)

    # on contruit la question, maintenant que l'on a la bonne réponse
    #   print("Construction de la question avec la bonne réponse")
    Question_i = Question(questions[i]['titre'], (
        questions[i]['choix'][0][0],
        questions[i]['choix'][1][0],
        questions[i]['choix'][2][0],
        questions[i]['choix'][3][0]), Bonne_rep)
    #   print(Question_i)
    Question_list.append(Question_i)  # il ne faut pas oublier de passer par un paramètre "question_i" qui correspond à
    # une question donné. Le paramètre "question" correspond lui à une classe. A chaque fin de boucle "i" on ajoute
    # la question à la liste des questions
    print(Question_list)

Questionnaire(  # on peut lui ajouter un tuple ou une liste indiférement. On lui donne la liste des questions définie
    # plus haut grâce à une boucle "for"
    Question_list
).lancer()


# ETAPE 1 : essayer de faire venir le fichier du code "import.py". En effet, il faut que je réussisse à faire le lien
# avec le fichier "import.py"
# En fait on va devoir charger les fichiers ".json" que l'on créer grâce à notre script d'import. Et c'est ces fichiers
# que l'on va utiliser dans le "questionnaire.py" afin de poser les questions

# PROBLEME RENCONTRE :
