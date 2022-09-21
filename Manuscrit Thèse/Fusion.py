
def fusion_biblio():
	with open('bib_thesis.bib','w') as mainBib:
		allItems=[]
		for i in range(1,5):
			bib=open('chapter %i/Bib_ch%i.bib'%(i,i),'r').read()
			bib=bib.split('@')
			for item in bib[1:]:
				item='@'+item
				if item not in allItems :
					allItems+=[item]
				else :
					pass
		for item in allItems:
			mainBib.write(item)

# fusion_biblio()

def en_tete(bibfile='bib_thesis.bib'):
	text='\\documentclass[a4paper,11pt]{report}\n\\usepackage[]{amsmath}\n\\usepackage[]{physics} % \\bra, \\ket etc\n\\usepackage{graphicx} %Pour les figures je crois\n\\usepackage{hyperref}\n\\usepackage[\n    backend=biber, \n    natbib=true,\n    style=numeric-comp,\n    sorting=none, %Pour faire apparaitre les refs dans l\'ordre\n    hyperref=true\n]{biblatex} %Imports biblatex package\n\\addbibresource{'+bibfile+'} %Import the bibliography file\n\n\\usepackage{amssymb} %quelques symboles dont gtrsim /lesssim\n\\usepackage{subcaption} % package pour faire des subfigures\n\\usepackage{multirow} % package pour multirow/multicolumn\n\\usepackage{booktabs} % package pour top/mid/bottom rule\n\\usepackage{tcolorbox} % toujours plus de boites\n\\usepackage{xcolor} % Pour avoir des couleurs dans les équations\n\n\\title{}\n\\begin{document}\n'
	return text
def closure():
	text='\\end{document}\n'
	return text

def fusion_chapters():
	with open('these_fusion.tex','w') as f:
		f.write(en_tete(bibfile='bib_thesis.bib'))
		for i in range(1,5):
			chap=open('chapter %i/Chapter %i.tex'%(i,i),'r').read()
			chap=chap.split('begin{document}')[1]
			chap=chap.split('end{document}')[0]
			chap=chap[:-2]
			chap=chap.replace('Figures/','chapter %i/Figures/'%i )
			chap='\\begin{refsection}\n'+chap+'\n\\end{refsection}\n '
			f.write(chap)
		f.write(closure())


fusion_chapters()