with open('courseid_3990_participants.csv','r') as f :
	mail=[]

	for line in f:
		line=line.split(',')
		mail+=[line[2]]



with open('liste_adresse.txt','w') as f :
	for elem in mail[1:] :
		f.write(elem+',')
