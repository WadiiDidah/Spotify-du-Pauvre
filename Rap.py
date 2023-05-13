
import Ice
import Example
import sys
import os

class RapServer(Example.MyInterface):
    def __init__(self):
        self.musiques = []

    def printMessage(self, message, current=None):
        print(message)

    def addMusique(self, genre, nom, auteur, current=None):
        with open("RAP/"+auteur+"-"+nom+".mp3", "rb") as file:
                    audio_data = file.read()

        

            # retourner les données audio
        return audio_data
    
    def getMusiques(self, current=None):
        return self.musiques
    
    def supprimerMusique(self,nom,auteur,current=None):
        try:
            # Vérifier si le fichier existe
            chemin = "musiques/" + auteur.lower() +"-"+nom.lower()+".mp3"
            if not os.path.exists(chemin):
                return False
            
            # Supprimer le fichier
            os.remove(chemin)
            return True
        
        except Exception as e:
            print("Erreur lors de la suppression de la musique:", e)
            return False
    
    def updateMusique(self, oldNom, nvNom, auteur,current=None):
        dossier = "musiques/"
        for filename in os.listdir(dossier):
            if filename.endswith(".mp3"):
                auteur, nom = filename[:-4].split("-")
                if nom.lower() == oldNom.lower() and auteur.lower()== auteur.lower():
                    oldPath = os.path.join(dossier, filename)
                    newPath = os.path.join(dossier, auteur + "-" + nvNom + ".mp3")
                    os.rename(oldPath, newPath)
                    return True
        return False
   


with Ice.initialize(sys.argv) as communicator:
    properties = communicator.getProperties()
    properties.setProperty("Ice.MessageSizeMax", "10485760")
    adapter = communicator.createObjectAdapterWithEndpoints("RapServer", "default -p 10000")
    object = RapServer()
    adapter.add(object, communicator.stringToIdentity("RapServer"))
    adapter.activate()
    communicator.waitForShutdown()
