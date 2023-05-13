import Ice
import sys
import Example
import os
import music_player

def get_proxy(type):
    proxy = None
    if type.upper() == "RAP":
        proxy = Example.MyInterfacePrx.checkedCast(communicator.stringToProxy("RapServer:default -p 10000"))
    elif type.upper() == "RNB":
        proxy = Example.MyInterfacePrx.checkedCast(communicator.stringToProxy("RnBServer:default -p 10001"))
    elif type.upper() == "ROCK":
        proxy = Example.MyInterfacePrx.checkedCast(communicator.stringToProxy("RockServer:default -p 10002"))
    else:
        print("Type de musique non reconnu")
        sys.exit(1)
    return proxy


if __name__ == "__main__":
    with Ice.initialize(sys.argv) as communicator:
        properties = communicator.getProperties()
        properties.setProperty("Ice.MessageSizeMax", "10485760")

        while True:
            type = input("Entrez le type de musique (RAP, RNB ou ROCK) : ")
            type = type.upper()
            proxy = get_proxy(type)

            if not proxy:
                continue

            while True:
                choix = input("== MENU ==\n\n1. Ajouter une musique\n2. Consulter ma musique\n3. Quitter\n\nEntrez votre choix : ")
                if choix == "1":
                    print("****la liste de musique ******\n\n")
                    musiques =  proxy.getMusiques(type)
                    i=0
                    for musique in musiques:
                        i+=1
                        print(str(i)+": "+musique+"\n")
                    nom = input("Nom : ")
                    auteur = input("Auteur : ")
                   
                    byte_seq = proxy.addMusique(type, nom, auteur)
                    if not os.path.exists("musiques"):
                        print("je suiss laaa2")
                        os.makedirs("musiques")
                    with open("musiques/"+auteur+"-"+nom+".mp3", "wb") as f:
                            print("je suiss laaa3")
                            f.write(byte_seq)
                    print("Musique ajoutée avec succès")
                elif choix == "2":
                    print("****Ma liste de musique ******\n\n")
                    musiques =  proxy.getFavoris()
                    i=0
                    for musique in musiques:
                        i+=1
                        print(str(i)+": "+musique+"\n")
                    choix2 = input("== MENU ==\n\n1. Ecouter ma musique\n2. Modifier ma musique\n3. Supprimer ma musique\n4. Quitter\n\nEntrez votre choix : ")
                    if choix2=="1":
                        nom = input("nom : ")
                        auteur = input("Auteur : ")
                        music_player.playMusic(nom,auteur)
                    elif choix2 == "2":
                        oldNom = input("Nom actuel : ")
                        nvNom = input("Nouveau nom : ")
                        auteur = input("Auteur : ")
                        result = proxy.updateMusique(oldNom, nvNom, auteur)
                        if result:
                            print("Musique modifiée avec succès")
                        else:
                            print("Impossible de modifier la musique")
                    elif choix2 =="3":
                        nom = input("Nom : ")
                        auteur = input("Auteur : ")
                        result = proxy.supprimerMusique(nom, auteur)
                        if result:
                            print("Musique supprimée avec succès")
                        else:
                            print("Impossible de supprimer la musique")
                    
                elif choix == "3":
                    sys.exit(0)
                else:
                    print("Choix invalide")