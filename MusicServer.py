import Ice
import Example
import sys
import os

class MusicServer(Example.MyInterface):
    def __init__(self, genre):
        self.genre = genre
        self.musiques = []

    def printMessage(self, message, current=None):
        print(message)

    def addMusique(self,genre,nom, auteur, current=None):
        with open(genre+"/"+auteur+"-"+nom+".mp3", "rb") as file:
            audio_data = file.read()
            # retourner les données audio
        return audio_data
    
    def getMusiques(self,genre,current=None):
        musiques = []
        for filename in os.listdir(genre):
            if filename.endswith(".mp3"):
                musiques.append(filename)
        return musiques
        
    
    def supprimerMusique(self,nom,auteur,current=None):
        try:
            # Vérifier si le fichier existe
            chemin =  "musiques/" + auteur.lower() +"-"+nom.lower()+".mp3"
            if not os.path.exists(chemin):
                return False
            
            # Supprimer le fichier
            os.remove(chemin)
            return True
        
        except Exception as e:
            print("Erreur lors de la suppression de la musique:", e)
            return False
    
    def updateMusique(self, oldNom, nvNom, auteur, current=None):
        dossier = "musiques/"
        for filename in os.listdir(dossier):
            if filename.endswith(".mp3"):
                file_auteur, file_nom = filename[:-4].split("-")
                if file_nom.lower() == oldNom.lower() and file_auteur.lower() == auteur.lower():
                    oldPath = os.path.join(dossier, filename)
                    newPath = os.path.join(dossier, auteur + "-" + nvNom + ".mp3")
                    os.rename(oldPath, newPath)
                    return True
        return False
    def getFavoris(self,current=None) :
        musiques = []
        for filename in os.listdir("musiques"):
            if filename.endswith(".mp3"):
                musiques.append(filename)
        return musiques


class RapServer(MusicServer):
    def __init__(self):
        super().__init__("RAP")
        
class RnBServer(MusicServer):
    def __init__(self):
        super().__init__("RnB")
        
class RockServer(MusicServer):
    def __init__(self):
        super().__init__("ROCK")

with Ice.initialize(sys.argv) as communicator:
    properties = communicator.getProperties()
    properties.setProperty("Ice.MessageSizeMax", "10485760")
    
    # Créer les adaptateurs pour chaque serveur
    rap_adapter = communicator.createObjectAdapterWithEndpoints("RapServer", "default -p 10000")
    rnb_adapter = communicator.createObjectAdapterWithEndpoints("RnBServer", "default -p 10001")
    rock_adapter = communicator.createObjectAdapterWithEndpoints("RockServer", "default -p 10002")
    
    # Ajouter les instances de chaque classe serveur à leur propre adaptateur
    rap_object = RapServer()
    rnb_object = RnBServer()
    rock_object = RockServer()
    
    rap_adapter.add(rap_object, communicator.stringToIdentity("RapServer"))
    rnb_adapter.add(rnb_object, communicator.stringToIdentity("RnBServer"))
    rock_adapter.add(rock_object, communicator.stringToIdentity("RockServer"))
    
    # Activer les adaptateurs
    rap_adapter.activate()
    rnb_adapter.activate()
    rock_adapter.activate()
    
    communicator.waitForShutdown()
