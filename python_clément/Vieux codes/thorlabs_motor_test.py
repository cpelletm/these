import thorlabs_apt as apt #Prend qq secondes pour importer les données moteur
import time

ml=apt.list_available_devices() #ml=[(31, 27254827), (31, 27255158)]

motor1 = apt.Motor(ml[0][1])
motor2 = apt.Motor(ml[1][1])


#motor1.move_home(True) # Bloquant par defaut
#motor1.move_to(0,blocking = False) # Lorsque non bloquant (le programe rend la main avant que le moteur ait finit de bouger), l'ordre le plus récent remplace le précédent
#time.sleep(1)
#motor1.move_to(5,blocking = False)




