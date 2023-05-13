import vlc

def playMusic(nom,auteur):
    # création d'une instance VLC
    instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
    player = instance.media_player_new()
    filepath = "musiques/"+auteur+"-"+nom+".mp3"
    # chargement du fichier audio
    media = instance.media_new(filepath)
    player.set_media(media)

    # démarrage de la lecture
    player.play()

    # boucle d'écoute des événements de l'utilisateur
    while True:
        command = input("Commande (play/pause/stop/exit): ")

        if command == "play":
            player.play()
        elif command == "pause":
            player.pause()
        elif command == "stop":
            player.stop()
           
        elif command == "exit":
            player.stop()
            instance.release()
            break

