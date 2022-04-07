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

    def from_json_data(data):  # ici on obligé de faire du code pour aller chercher les réponse
        # QUESTIONS
        ques = data["titre"]
        #  print(ques)

        # CHOIX
        choix = [i[0] for i in data["choix"]]  # on fait une complétion de liste
        # print(choix)
        # print(len(choix))

        # BONNE REPONSE
        # pour comprendre
        #   print(data["choix"])
        #   print(data["choix"][1])
        #   print(data["choix"][1][1])

        # PARTIE QUI PEUT ETRE REMPLACE PAR UNE COMPLETION
        # bonne_rep = None
        #for i in range(0, 4):
          #  print(i)
           # print(data["choix"][i][1])
            #print(data["choix"][i][0])
        #    if data["choix"][i][1]:
             #   print("VRAI")
         #       bonne_rep = data["choix"][i][0]
              #  print(bonne_rep)
        # print(bonne_rep)

        bonne_reponse = [i[0] for i in data["choix"] if i[1]]
        #   print(bonne_reponse[0])
        if len(bonne_reponse) != 1:
            return None  # si la longueur de la bonne réponse est différent de 1 c'est qu'on a un pb

        # CONSTRUCTION DE LA QUESTION : avec "ques", "choix", "bonne_reponse"
        q = Question(ques, choix, bonne_reponse[0])  # on utilise la syntaxe d'avant que l'on retravaillé
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
    
    def __init__(self, questions, titre, categorie, difficulte):
        self.questions = questions
        self.titre = titre
        self.categorie = categorie
        self.difficulte = difficulte

    def from_json_data(data):  # c'est ici qu l'on va réunir les infos du questionnaire
        liste_des_questions = data["questions"]  # toutes les questions du dictionnaire
        questions = [Question.from_json_data(i) for i in liste_des_questions]
        #  "questions" = ["question créée n°i" for i in "liste des questions"]
        # i correspond à un élément dans "liste de question"
        return Questionnaire(questions, data["titre"], data["categorie"], data["difficulte"])
        # on peut lui ajouter un tuple ou une liste indiférement

    def lancer(self):
        print("----------> ")
        print("QUESTIONNAIRE : " + self.titre)
        print("Catégorie : " + self.categorie)
        print("Difficulté : " + self.difficulte)
        print("Nombre de question : " + str(len(self.questions)))
        print("----------> ")
        score = 0
        for question in self.questions:
            self.numero_question += 1
            print("QUESTION N°" + str(self.numero_question) + " / " + str(len(self.questions)))  # on met ce
            # "print" ici pour avoir le numéro de la question
            if question.poser():
                score += 1
        print("Score final :", score, "sur", len(self.questions))
        return score


# NOUVEAU TRAVAIL / les fichiers "json" que l'on récupère sont au format texte
f = open("gastronomie_chocolat_expert.json", "r")  # on ouvre le fichier json avec toutes les questions et réponse
f_reading = f.read()  # on créé un fichier de lecture
f_reading_dico = json.loads(f_reading)  # on désérialise : "texte -> dico". C'est un dictionnaire dans lequel on a
# toutes les questions (on aura pu le faire après le "close" si on le souhaitais)
f.close()  # on a tout copié dans le dico "f_reading_dico" on peut fermer le fichier texte

# on récupère les données du dico
#  liste_des_questions = f_reading_dico["questions"]  # toutes les questions du dictionnaire
# ON POSE UNE QUESTION SEULE ICI
# q = Question.FromJsonData(liste_des_questions[0])  # on appelle la fonction "FromJsonData" de la classe "Question"
# (rq : on aurait pu choisir de changer l'init de "Question", mais on a préféré changer le pattern entier)
# print(type(q))
# print(q)
# q.poser()  # on pose cette question

# DONNEES de compréhension
#   categorie_questionnaire = f_reading_dico["categorie"]  # la catégorie du quizz
#   titre_questionnaire = f_reading_dico["titre"]  # la titre du quizz
#   difficulte_questionnaire = f_reading_dico["difficulte"]  # la difficulté du quizz
#   print(categorie)
#   print(titre)
#   print(questions[1]['titre'])  # question 2
#   print(questions[3]['choix'])  # tous les choix choix de la question 4
#   print(questions[5]['choix'][0][0])  # Choix 1 de la question 6
#   print(questions[5]['choix'][2][0])  # Choix 3 de la question 6

# METHODE AVEC BOUBLE FOR que l'on a fait eovuler avec une comletion juste en dessous
"""Question_list = []
print(liste_des_questions)
print(len(liste_des_questions))
for i in range(0, len(liste_des_questions)): 
    q = Question.FromJsonData(liste_des_questions[i])
    Question_list.append(q)
    print(Question_list)
    
Questionnaire(Question_list).lancer()  # on peut lui ajouter un tuple ou une liste indiférement"""

# ENCORE une fois cette boucle for peut être faite par un COMPLETION de liste
Questionnaire.from_json_data(f_reading_dico).lancer()
# avec cette simple commande on peut lancer un questionnaire sur différents questionnaires

# METHODE INITIALE : on avait codé à l'extérieur de la calsse question
"""Question_list = []
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
).lancer()"""


# ETAPE 1 : essayer de faire venir le fichier du code "import.py". En effet, il faut que je réussisse à faire le lien
# avec le fichier "import.py"
# En fait on va devoir charger les fichiers ".json" que l'on créer grâce à notre script d'import. Et c'est ces fichiers
# que l'on va utiliser dans le "questionnaire.py" afin de poser les questions. Ces fichiers se chargent comme un fichier
# texte
# On a chargé un fichier "json", désériliaser les données et fait tourner la question à partir des données qui sont dans
# le fichier. C'est à dire que l'on va récupérer des données texte et on va les mettre sous forme d'un dico


# ETAPE 2 : a pu poser une questionen retravaillant un peu le classe "qestion", on va désromais lancer toute les
# questions à partir de la classe questionnaire


# PROBLEME RENCONTRE :

