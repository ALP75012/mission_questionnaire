import requests
import json
import unicodedata

open_quizz_db_data = (
        ("Animaux", "Les chats", "https://www.kiwime.com/oqdb/files/1050288832/OpenQuizzDB_050/openquizzdb_50.json"),
        ("Arts", "Musée du Louvre", "https://www.kiwime.com/oqdb/files/1086665427/OpenQuizzDB_086/openquizzdb_86.json"),
        ("Bande dessinnée", "Tintin", "https://www.kiwime.com/oqdb/files/2124627594/OpenQuizzDB_124/openquizzdb_124.json"),
        ("Gastronomie", "Chocolat", "https://www.kiwime.com/oqdb/files/1019678723/OpenQuizzDB_019/openquizzdb_19.json"),
        ("Cinéma", "Star wars", "https://www.kiwime.com/oqdb/files/1090683544/OpenQuizzDB_090/openquizzdb_90.json"),
)


# FICHIERS INITIAUX QUI SONT TOUS IMPOSSIBLES A DESERIALISE
#open_quizz_db_data = (
 #   ("Animaux", "Les chats", "https://www.kiwime.com/oqdb/files/1050828847/OpenQuizzDB_050/openquizzdb_50.json"),
  #  ("Arts", "Musée du Louvre", "https://www.kiwime.com/oqdb/files/1086624389/OpenQuizzDB_086/openquizzdb_86.json"),
   # ("Bande dessinnée", "Tintin", "https://www.kiwime.com/oqdb/files/2124627384/OpenQuizzDB_124/openquizzdb_124.json"),
    #("Cinéma", "Alien", "https://www.kiwime.com/oqdb/files/3241454997/OpenQuizzDB_241/openquizzdb_241.json"),
    #("Cinéma", "Star wars", "https://www.kiwime.com/oqdb/files/1090993427/OpenQuizzDB_090/openquizzdb_90.json"),
#)


# POUR REALISER DES ESSAIS
#open_quizz_db_data = (
 #       ("Animaux", "Les chats", "https://www.kiwime.com/oqdb/files/1050288832/OpenQuizzDB_050/openquizzdb_50.json"),
  #      ("essais", "CEci est un essai", "https://www.kiwime.com/9oqdb/files/1050288832/OpenQuizzDB_050/openquizzdb_50.json")
#)


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def get_quizz_filename(categorie, titre, difficulte):
    return strip_accents(categorie).lower().replace(" ", "") + "_" + strip_accents(titre).lower().replace(" ", "") + "_" + strip_accents(difficulte).lower().replace(" ", "") + ".json"


def generate_json_file(categorie, titre, url):  # cette fonction permet de prendre les données texte initiale de les
    # traiter en les mettant dans le bon ordre et renvoyer un fichier "texte" global" "out_json"
    #   print("DEBUT FONCTION. Elle est appelée autant de fois qu'il y'a de fichiers à importer")
    #   print()
    out_questionnaire_data = {"categorie": categorie, "titre": titre, "questions": []}
    #   print(out_questionnaire_data)
    out_questions_data = []
    try:  # on met un condition "try" pour voir si on arrive à récupérer les url
        response = requests.get(url)  # on récupère l'url
        print("URL : " + url + " RECUPERE")
    #   print("LES DATAS SERIALISES (sous forme de texte) SONT")
    #   print(response.text)  # il y'a 30 questions
    #   print(type(response.text))
    except:
        print("URL : " + url + " n'est pas correct")
        print("Il y'a un problème dans cette partie '" + url[0:23] + "' de l'url")
    else:
        try:
            data = json.loads(response.text)  # on désérialise les données "reponse" : text --> dico
            print("Questionnaire sur les ' " + categorie + " ' RECUPERE")
            #   print(type(data))
            #   print("LES DATAS DESERIALISES (sous forme de dictionnaire) SONT")
            #   print(data)
        except:
            print("Questionnaire sur les ' " + categorie + " ' IMPOSSIBLE à DESERIALISER")
        else:
            all_quizz = data["quizz"]["fr"]  # correspond au différents quizz : il y'a 3 : car 3 niveaux de difficulté
            #   print("LES DATAS 'all_quizz' SONT")
            #   print(all_quizz)
            #   print(len(all_quizz))
            for quizz_title, quizz_data in all_quizz.items():
                out_filename = get_quizz_filename(categorie, titre, quizz_title)
                #   print(out_filename)  # on écrit le nom de sortie
                out_questionnaire_data["difficulte"] = quizz_title
                #   print("LES DATAS 'out_questionnaire_data' SONT")
                #   print(quizz_title)
                for question in quizz_data:  # "quizz_data" correspond au 10 question débutant, puis au 10 question confirmé, e
                    question_dict = {}
                    question_dict["titre"] = question["question"]
                    question_dict["choix"] = []
                    for ch in question["propositions"]:
                        question_dict["choix"].append((ch, ch==question["réponse"]))
                    out_questions_data.append(question_dict)
                out_questionnaire_data["questions"] = out_questions_data
                out_json = json.dumps(out_questionnaire_data)  # on sérialise "out_questionnaire_data" -> texte
                #   print("LES DATAS 'out_json' (en mode texte)  SONT")
                # print(out_json)  # on additionne les données du questionnaire débutant puis du cofirmé,
                # puis du expert à chaque tour de boucle
                #   print(type(out_json))

                # le "out_json" final est un fichier texte contenant toute les données des 3 questionnaires on
                # écrit toutes ces données dans un fichier texte appelé "out_filename"
                # out_filename = get_quizz_filename(categorie, titre, quizz_title) avec ceci on va dans la fonction
                # qui permet d'obtenir un fichier "filename"
                file = open(out_filename, "w")  # ouerture du fichier en écriture
                file.write(out_json)
                file.close()

                # là j'ai décidé d'écrire mes données sur un fichier texte pour voir ce que cela donne réellement
                # file = open("mon_fichier_txt_avec_question", "w")
                # file.write(out_json)
                # file.close()

                #   print("end")
                #   print(out_questions_data)
                #   print(out_questions_data[0])  # question 1
                #   print(out_questionnaire_data)
                #   print(out_questions_data[4])  # question 5
            print()


for quizz_data in open_quizz_db_data:
    generate_json_file(quizz_data[0], quizz_data[1], quizz_data[2])


# ETAPE 1 : debugguer le code. L'idée est que le code que tourne
# le problème que l'on avait rencontré est que certains liens n'étaient plus à jour. la solution est alors de tester si
# les liens peuvent être ouvert avant de de les ouvrir

# ETAPE 2 : on va charger un fichier. obtenir les données, les désérialisées et faire tourner le fichier "qestionnaire"
# à partir des données qui sont dans le fichier / en fait le fichier chat par ex est un questionnaire à part entière

# PROBLEME RENCONTRE :
# fair ele lien entre mes deux fichiers ".py" afin de lui transmettre les questionnaires que j'ai recu d'internet à la
# partie sur les questionnaire qui va le traiter comme je le souhaite.

# REMARQUES :
# écrire ces catégories : étapes, problème rencontré, remarque est utile dans les projets que je récupére pour avancer
# pas à pas

