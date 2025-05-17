import speech_recognition as sr
import pyttsx3
import webbrowser
import random
from datetime import datetime

# Initialisation de Jarvis
engine = pyttsx3.init()
engine.setProperty('rate', 160)

# Voix masculine si dispo
voices = engine.getProperty('voices')
for voice in voices:
    if "male" in voice.name.lower() or "homme" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

def parler(text):
    engine.say(text)
    engine.runAndWait()

def takecommand():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nMicro ouvert, en train d'écouter...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Audio capturé")
        except sr.WaitTimeoutError:
            print("Aucun son détecté.")
            return ""

    try:
        query = recognizer.recognize_google(audio, language="fr-FR")
        print("Vous avez dit :", query)
        return query.lower()

    except Exception as e:
        print("Erreur de reconnaissance :", e)
        return ""

def raconter_blague():
    blagues = [
        "Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce que sinon ils tombent dans le bateau.",
        "Que dit une imprimante dans l’eau ? J’ai papier !",
        "Pourquoi les canards ont-ils autant de plumes ? Pour couvrir leur derrière.",
        "Quel est le comble pour un électricien ? De ne pas être au courant.",
        "Quelle browleur choisi un arabe ? Dynamike !"
    ]
    parler(random.choice(blagues))

def calcul_simple(phrase):
    phrase = phrase.replace("plus", "+").replace("moins", "-").replace("fois", "*").replace("divisé par", "/")
    try:
        result = eval(phrase)
        parler(f"Le résultat est {result}")
    except:
        parler("Désolé, je n'ai pas compris le calcul.")

def jouer_sur_spotify(commande):
    recherche = commande.replace("joue", "").strip()
    if recherche:
        url = f"https://open.spotify.com/search/{recherche.replace(' ', '%20')}"
        webbrowser.open(url)
        parler(f"Voici {recherche} sur Spotify.")
    else:
        parler("Tu dois dire ce que tu veux écouter.")

def assistant():
    parler("Bonjour, je suis Jarvice pour Android. Je suis à votre écoute.")
    while True:
        commande = takecommand()

        if "quelle heure est-il" in commande:
            now = datetime.now()
            parler(f"Il est {now.strftime('%H:%M:%S')}")

        elif "quel jour sommes-nous" in commande:
            parler(f"Nous sommes le {datetime.now().strftime('%A %d %B %Y')}")

        elif "ouvre google" in commande:
            webbrowser.open("https://www.google.com")
            parler("Google est ouvert.")

        elif "ouvre youtube" in commande:
            webbrowser.open("https://www.youtube.com")
            parler("YouTube est ouvert.")

        elif "raconte une blague" in commande or "dis une blague" in commande:
            raconter_blague()

        elif "quelle est la météo" in commande:
            parler("Je ne peux pas encore donner la météo en direct, mais je m'y prépare.")

        elif "fais un calcul" in commande:
            parler("Quel calcul souhaitez-vous faire ?")
            calcul = takecommand()
            calcul_simple(calcul)

        elif "joue" in commande:
            jouer_sur_spotify(commande)

        elif "lance une musique" in commande:
            webbrowser.open("https://www.youtube.com/results?search_query=musique")
            parler("Voici quelques musiques sur YouTube.")

        elif "cherche" in commande:
            recherche = commande.replace("cherche", "").strip()
            if recherche:
                url = f"https://www.google.com/search?q={recherche}"
                webbrowser.open(url)
                parler(f"Voici les résultats pour {recherche}")
            else:
                parler("Que voulez-vous que je cherche ?")

        elif "comment tu t'appelles" in commande or "qui es-tu" in commande:
            parler("Je suis Jarvice, votre assistant vocal personnel.")

        elif "arrête" in commande or "stop" in commande:
            parler("Très bien. À bientôt.")
            break

        elif commande != "":
            parler("Je ne sais pas encore répondre à ça, mais je m'améliore chaque jour.")

# Lancement
assistant()