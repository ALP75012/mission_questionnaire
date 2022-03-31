import requests
import json
import unicodedata


# le but de ceci est de venir convertir les données que l'on récupère dans un format qui est égal ou proche de ce que l'on a fait dans le projet questionnaire
# pour chaque lien on va pouvoir extraire 3 quiz en fonction des niveau de diffcultés
# 1ere chose  àfaire  :reparer ce code : pourquoi ça ne marche plus. Si on fait "ls" on voit tous les fichiers "json" qui ont servie pour l'import. Si on souhaite
# que les fichiers "json" soit généré dans le même fichier que le script
# une fois que l'on a les fichiers au format json dans notre import, l'idée va être de pouvoir
# les ouvrir dans notre onglet questionnaire


#open_quizz_db_data = (
     #   ("Animaux", "Les chats", "https://www.kiwime.com/oqdb/files/1050288832/OpenQuizzDB_050/openquizzdb_50.json"),
    #    ("Arts", "Musée du Louvre", "https://www.kiwime.com/oqdb/files/1086665427/OpenQuizzDB_086/openquizzdb_86.json"),
   #     ("Bande dessinnée", "Tintin", "https://www.kiwime.com/oqdb/files/2124627594/OpenQuizzDB_124/openquizzdb_124.json"),
  #      ("Gastronomie", "Chocolat", "https://www.kiwime.com/oqdb/files/1019678723/OpenQuizzDB_019/openquizzdb_19.json"),
 #       ("Cinéma", "Star wars", "https://www.kiwime.com/oqdb/files/1090683544/OpenQuizzDB_090/openquizzdb_90.json"),
#)


open_quizz_db_data = (
        ("Animaux", "Les chats", "https://www.kiwime.com/oqdb/files/1050288832/OpenQuizzDB_050/openquizzdb_50.json"),
        ("Animaux", "Les chats", "https://www.kiwime.com/oqdb/files/1050288832/OpenQuizzDB_050/openquizzdb_50.json")
)


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def get_quizz_filename(categorie, titre, difficulte):
    return strip_accents(categorie).lower().replace(" ", "") + "_" + strip_accents(titre).lower().replace(" ", "") + "_" + strip_accents(difficulte).lower().replace(" ", "") + ".json"


def generate_json_file(categorie, titre, url):  # cette fonction permet de prendre les données texte intiale de les
    # traiter en les mettant dans le bon ordre et renvoyer un fichier "texte" global" "out_json"
    out_questionnaire_data = {"categorie": categorie, "titre": titre, "questions": []}
    print(out_questionnaire_data)
    out_questions_data = []
    response = requests.get(url)
  #  print("LES DATAS SERIALISES (sous forme de texte) SONT")
   # print(response.text)  # il y'a 30 questions
   # print(type(response.text))
    data = json.loads(response.text)  # on désérialise les données "reponse". on passe : text à dico
   # print(type(data))
  #  print("LES DATAS DESERIALISES (sous forme de dictionnaire) SONT")
   # print(data)
    all_quizz = data["quizz"]["fr"]  # correspond au différents quizz : il y'a 3 : car 3 niveaux de difficulté
  #  print("LES DATAS 'all_quizz' SONT")
  #  print(all_quizz)
  #  print(len(all_quizz))
    for quizz_title, quizz_data in all_quizz.items():
        out_filename = get_quizz_filename(categorie, titre, quizz_title)
       # print(out_filename)  # on écrit le nom de sortie
        out_questionnaire_data["difficulte"] = quizz_title
       # print("LES DATAS 'out_questionnaire_data' SONT")
       # print(quizz_title)
        for question in quizz_data:  # "quizz_data" correspond au 10 question débutant, puis au 10 question confirmé, e
            question_dict = {}
            question_dict["titre"] = question["question"]
            question_dict["choix"] = []
            for ch in question["propositions"]:
                question_dict["choix"].append((ch, ch==question["réponse"]))
            out_questions_data.append(question_dict)
        out_questionnaire_data["questions"] = out_questions_data
        out_json = json.dumps(out_questionnaire_data)  # on sérialise les données "out_questionnaire_data" -> texte
       # print("LES DATAS 'out_json' (en mode texte)  SONT")
        print(out_json)  # on additionne les données du questionnaire débutant puis du cofirmé, puis du expert

        print(type(out_json))
        # le "out_json" final est un fichier texte contenant toute les données des 3 questionnaires
        # on écrit toutes ces données dans un fichier texte appelé "out_filename"
        # out_filename = get_quizz_filename(categorie, titre, quizz_title) avec ceci on va dans la fonction qui permet
        # d'obtenir un fichier "filename"
        file = open(out_filename, "w")
        file.write(out_json)
        file.close()
        # là j'ai décidé d'écrire mes données sur un fichier texte pour voir ce que cela donne réellement
        file = open("mon_fichier_txt_avec_question", "w")
        file.write(out_json)
        file.close()

       # print("end")
  #  print(out_questions_data)
  #  print(out_questions_data[0])  # question 1
  #  print(out_questionnaire_data)
   # print(out_questions_data[1])  # question 2
   # print(out_questions_data[3])  # question 3
   # print(out_questions_data[4])  # question 4
   # print(out_questions_data[5])  # question 5
   # print(out_questions_data[6])  # question 6
   # print(out_questions_data[7])  # question 7
   # print(out_questions_data[8])  # question 8
    # il y'a ue bon nom de question dans ce questionnaire : sous forme d'un dictionnaire
   # dico_calssique = out_questions_data[0]
   # dico_calssique = json.loads(t)
    print()

for quizz_data in open_quizz_db_data:
    generate_json_file(quizz_data[0], quizz_data[1], quizz_data[2])



# ETAPE 1 : debugguer le code. L'idée est que le code que tourne

# le problèmeque l'on avaut rencontré est que certains liens n'étais plus à jour
# "https://www.kiwime.com/oqdb/files/1019678723/OpenQuizzDB_019/openquizzdb_19.json"  : OK : chocolat
#  " https://www.kiwime.com/oqdb/files/1050288832/OpenQuizzDB_050/openquizzdb_50.json" : ok : chat
#  "https://www.kiwime.com/oqdb/files/1086665427/OpenQuizzDB_086/openquizzdb_86.json"  : Ok : musée du louvre
#  "https://www.kiwime.com/oqdb/files/2124627594/OpenQuizzDB_124/openquizzdb_124.json"  : ok : tintin
#  https://www.kiwime.com/oqdb/files/1090683544/OpenQuizzDB_090/openquizzdb_90.json  : ok : starwars

# ETAPE 2 : on va charger un fichier. obtenir les données, les désérialisées et faire tourner le fichier "qestionnaire"
# à partir des données qui sont dans le fichier
# en fait le fichier chat par exemple est un questionnaire à part entière



# PROBLEME RENCONTRE :
# fair ele lien entre mes deux fichiers ".py" afin de lui transmettre les questionnaires que j'ai recu d'internet à la
# partie sur les questionnaire qui va le traiter comme je le souhaite.

