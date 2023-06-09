#!/usr/bin/env python
#
# Copyright (c) ZeroC, Inc. All rights reserved.
#

import signal
import sys
import Ice
import IceStorm
import getopt
import os

Ice.loadSlice('Clock.ice')
import Demo


class ClockI(Demo.Clock):
    def tick(self,message, current):
        print(message)
    def addMusique(self,genre,nom, auteur, current=None):
        with open(r"../APPLICATION/"+auteur+"-"+nom+".mp3", "rb") as file:

            audio_data = file.read()
            # retourner les données audio
        if not os.path.exists(genre):
                os.makedirs(genre)
        with open(r"../APPLICATION/"+genre+"/"+auteur+"-"+nom+".mp3", "wb") as f:
                    f.write(audio_data)
        print("la musique a été ajouté")
    
    
    def supprimerMusique(self,genre,nom,auteur,current=None):
       
        # Vérifier si le fichier existe
        chemin ="../APPLICATION/"+genre+"/"+auteur+"-"+nom+".mp3"
        # Supprimer le fichier
        os.remove(chemin)
        print("La musique " +auteur+"-"+nom+".mp3 a été suppriméeé")
        
    
    def updateMusique(self, genre,oldNom, nvNom, auteur, current=None):
        
        dossier = "../APPLICATION/"+genre+"/"
        for filename in os.listdir(dossier):
            if filename.endswith(".mp3"):
                file_auteur, file_nom = filename[:-4].split("-")
                if file_nom.lower() == oldNom.lower() and file_auteur.lower() == auteur.lower():
                    oldPath = os.path.join(dossier, filename)
                    newPath = os.path.join(dossier, auteur + "-" + nvNom + ".mp3")
                    os.rename(oldPath, newPath)
                    print("la musique " +auteur+"-"+oldNom+".mp3  est devenu "+  auteur+"-"+nvNom+" .mp3 ")
                    
        
    


def usage():
    print("Usage: " + sys.argv[0] +
          " [--batch] [--datagram|--twoway|--ordered|--oneway] [--retryCount count] [--id id] [topic]")


def run(communicator):
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ['datagram', 'twoway', 'oneway', 'ordered', 'batch',
                                                      'retryCount=', 'id='])
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    batch = False
    option = "None"
    topicName = "time"
    id = ""
    retryCount = ""

    for o, a in opts:
        oldoption = option
        if o == "--datagram":
            option = "Datagram"
        elif o == "--twoway":
            option = "Twoway"
        elif o == "--ordered":
            option = "Ordered"
        elif o == "--oneway":
            option = "Oneway"
        elif o == "--batch":
            batch = True
        elif o == "--id":
            id = a
        elif o == "--retryCount":
            retryCount = a
        if oldoption != option and oldoption != "None":
            usage()
            sys.exit(1)

    if len(args) > 1:
        usage()
        sys.exit(1)

    if len(args) > 0:
        topicName = args[0]

    if batch and (option in ("Twoway", "Ordered")):
        print(sys.argv[0] + ": batch can only be set with oneway or datagram")
        sys.exit(1)

    manager = IceStorm.TopicManagerPrx.checkedCast(communicator.propertyToProxy('TopicManager.Proxy'))
    if not manager:
        print(args[0] + ": invalid proxy")
        sys.exit(1)

    #
    # Retrieve the topic.
    #
    try:
        topic = manager.retrieve(topicName)
    except IceStorm.NoSuchTopic as e:
        try:
            topic = manager.create(topicName)
        except IceStorm.TopicExists as ex:
            print(sys.argv[0] + ": temporary error. try again")
            sys.exit(1)

    adapter = communicator.createObjectAdapter("Clock.Subscriber")

    #
    # Add a servant for the Ice object. If --id is used the identity
    # comes from the command line, otherwise a UUID is used.
    #
    # id is not directly altered since it is used below to detect
    # whether subscribeAndGetPublisher can raise AlreadySubscribed.
    #

    subId = Ice.Identity()
    subId.name = id
    if len(subId.name) == 0:
        subId.name = Ice.generateUUID()
    subscriber = adapter.add(ClockI(), subId)

    #
    # Activate the object adapter before subscribing.
    #
    adapter.activate()

    qos = {}
    if len(retryCount) > 0:
        qos["retryCount"] = retryCount

    #
    # Set up the proxy.
    #
    if option == "Datagram":
        if batch:
            subscriber = subscriber.ice_batchDatagram()
        else:
            subscriber = subscriber.ice_datagram()
    elif option == "Twoway":
        # Do nothing to the subscriber proxy. Its already twoway.
        pass
    elif option == "Ordered":
        # Do nothing to the subscriber proxy. Its already twoway.
        qos["reliability"] = "ordered"
    elif option == "Oneway" or option == "None":
        if batch:
            subscriber = subscriber.ice_batchOneway()
        else:
            subscriber = subscriber.ice_oneway()

    try:
        topic.subscribeAndGetPublisher(qos, subscriber)
    except IceStorm.AlreadySubscribed:
        # This should never occur when subscribing with an UUID
        assert(id)
        print("reactivating persistent subscriber")

    communicator.waitForShutdown()

    #
    # Unsubscribe all subscribed objects.
    #
    topic.unsubscribe(subscriber)


#
# Ice.initialize returns an initialized Ice communicator,
# the communicator is destroyed once it goes out of scope.
#
with Ice.initialize(sys.argv, "config.sub") as communicator:
    #
    # Install a signal handler to shutdown the communicator on Ctrl-C
    #
    signal.signal(signal.SIGINT, lambda signum, frame: communicator.shutdown())
    if hasattr(signal, 'SIGBREAK'):
        signal.signal(signal.SIGBREAK, lambda signum, frame: communicator.shutdown())
    status = run(communicator)
