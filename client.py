import Ice
import Example
import sys
import os

props = Ice.createProperties()
props.setProperty('Ice.Override.Timeout', '10000') # 10 seconds
initData = Ice.InitializationData()
initData.properties = props
with Ice.initialize(sys.argv ) as communicator:
    
    base = communicator.stringToProxy("RapServer:default -p 10000")
    my_interface = Example.MyInterfacePrx.checkedCast(base)
    if not my_interface:
        raise RuntimeError("Invalid proxy")
    
    byte_seq = my_interface.addMusique("RAP", "miff", "Anas")
    if not os.path.exists("musiques"):
        os.makedirs("musiques")
    with open("musiques/mons-da.mp3", "wb") as f:
        f.write(byte_seq)
    modifier_etat= my_interface.updateMusique("TeSt","La miff","Anass")
    if modifier_etat :
        print ("la modification a été faite")
    supprimer_etat= my_interface.supprimerMusique("da","mons")
    if supprimer_etat :
        print("la musique a été supprimée")
    