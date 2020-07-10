Mesure de PL en fonction du champ mag.

1ere serie de mesure : Taux de PL, ESR et T1 en fonction de l'orientation de l'aimant. Pour l'instant le T1 j'y arrive pas

2e serie : Modification de la PL en fonction de l'intensité pour les deux cas limites (tout dégénérés et tout séparés). 
Pb : l'ESR chauffe les fils et modifie la PL (car dillatation thermique etc) sur des temps longs. Il faut trouver un moyen de s'assurer qu'on est dans la bonne dégénérescence : soit avec la PL (le plus simple, pas forcément rigoureux), soit avec le temps de vie (galère et pas plus rigoureux), soit en attendant longtemps après l'ESR (le setup magnétique a l'air stable dans le temps), mais cb de temps ? Mesure de la PL sur des temps longs, ça doit se faire. Sauf que ça règle pas le pb : tu dois faire un ESR entre tes deux mesures, et ca va changer les valeurs absolues de la PL d'une série à l'autre. Ca vaut quand meme le coup de regarder si la PL change bcp avec un ESR avec un petit courant (genre -30 dbm).

3e série : Mesure de t1 : les deux premières séries (faible puissance(t_polarisation = 150µs, P_vert= 10µW), pics dégénérés puis séparés) semblent montrer que la photoionisation est dominante sur la polarisation pour des puissances trop faibles/temps de pola trop courts). 
Ca me semble a priori cohérent avec le fait que le temps carac de photoionisation est plus rapide que le temps carac de polarisation des NV. Après le soucis c'est que moi, ce que je connais c'est le temps de desexcitation pour les deux processus (le t1 et le temps de monté au début). Mais est-ce que c'est la même chose le temps de thermalisation quand tu excites ? Et est-ce que ça dépend de la puissance de l'excitation ?

Finalement je raconte peut-etre des conneries, je viens de faire une courbe avec plus de puissance et plus de temps de pola et l'effet semble bcp plus important. (série 3 : P=20 µW et t_pola = 300µs, toujours spins séparés).

Serie 4 : P=20 µW et t_pola = 300µs, spins dégénérés : Comme à faible puissance, on voit une croissance a priori de photoionisation, mais par rapport au cas séparés, on ne voit pas de décroissance aux temps long. Ca peut être du au fait qu'elle soit trop courte, et donc cachée par les phénomène de photo-ionisation

Je fais une dernière série de mesure avec P~150 µW et 3=300 µs (en remettant la densité, j'espère que ça modifie pas le t1 ces conneries). Pour l'instant je vois un truc qui décroit. Fin en gros je vois cette fois ci un effet bcp plus fort pour le t1 que pour la photo-ionisation. En vrai la décroissance est linéaire, à creuser demain.

Je viens de faire un ESR, et les deux dernières mesures c'est dégénérés 2x2 (je pense)