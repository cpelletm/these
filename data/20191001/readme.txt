Mesure de PL en fonction du champ mag.

1ere serie de mesure : Taux de PL, ESR et T1 en fonction de l'orientation de l'aimant. Pour l'instant le T1 j'y arrive pas

2e serie : Modification de la PL en fonction de l'intensit� pour les deux cas limites (tout d�g�n�r�s et tout s�par�s). 
Pb : l'ESR chauffe les fils et modifie la PL (car dillatation thermique etc) sur des temps longs. Il faut trouver un moyen de s'assurer qu'on est dans la bonne d�g�n�rescence : soit avec la PL (le plus simple, pas forc�ment rigoureux), soit avec le temps de vie (gal�re et pas plus rigoureux), soit en attendant longtemps apr�s l'ESR (le setup magn�tique a l'air stable dans le temps), mais cb de temps ? Mesure de la PL sur des temps longs, �a doit se faire. Sauf que �a r�gle pas le pb : tu dois faire un ESR entre tes deux mesures, et ca va changer les valeurs absolues de la PL d'une s�rie � l'autre. Ca vaut quand meme le coup de regarder si la PL change bcp avec un ESR avec un petit courant (genre -30 dbm).

3e s�rie : Mesure de t1 : les deux premi�res s�ries (faible puissance(t_polarisation = 150�s, P_vert= 10�W), pics d�g�n�r�s puis s�par�s) semblent montrer que la photoionisation est dominante sur la polarisation pour des puissances trop faibles/temps de pola trop courts). 
Ca me semble a priori coh�rent avec le fait que le temps carac de photoionisation est plus rapide que le temps carac de polarisation des NV. Apr�s le soucis c'est que moi, ce que je connais c'est le temps de desexcitation pour les deux processus (le t1 et le temps de mont� au d�but). Mais est-ce que c'est la m�me chose le temps de thermalisation quand tu excites ? Et est-ce que �a d�pend de la puissance de l'excitation ?

Finalement je raconte peut-etre des conneries, je viens de faire une courbe avec plus de puissance et plus de temps de pola et l'effet semble bcp plus important. (s�rie 3 : P=20 �W et t_pola = 300�s, toujours spins s�par�s).

Serie 4 : P=20 �W et t_pola = 300�s, spins d�g�n�r�s : Comme � faible puissance, on voit une croissance a priori de photoionisation, mais par rapport au cas s�par�s, on ne voit pas de d�croissance aux temps long. Ca peut �tre du au fait qu'elle soit trop courte, et donc cach�e par les ph�nom�ne de photo-ionisation

Je fais une derni�re s�rie de mesure avec P~150 �W et 3=300 �s (en remettant la densit�, j'esp�re que �a modifie pas le t1 ces conneries). Pour l'instant je vois un truc qui d�croit. Fin en gros je vois cette fois ci un effet bcp plus fort pour le t1 que pour la photo-ionisation. En vrai la d�croissance est lin�aire, � creuser demain.

Je viens de faire un ESR, et les deux derni�res mesures c'est d�g�n�r�s 2x2 (je pense)