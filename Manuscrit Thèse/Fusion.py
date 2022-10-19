
def fusion_biblio():
	with open('bib_thesis.bib','w') as mainBib:
		allItems=[]
		bibfiles=['chapter %i/Bib_ch%i.bib'%(i,i) for i in range(1,5)]+['Intro et conclusion/bib_intro.bib']
		for file in bibfiles:
			bib=open(file,'r').read()
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

def en_tete_simple(bibfile='bib_thesis.bib'):
	text='\\documentclass[a4paper,11pt]{report}\n\\usepackage[]{amsmath}\n\\usepackage[]{physics} % \\bra, \\ket etc\n\\usepackage{graphicx} %Pour les figures je crois\n\\usepackage{hyperref}\n\\usepackage[\n    backend=biber, \n    natbib=true,\n    style=numeric-comp,\n    sorting=none, %Pour faire apparaitre les refs dans l\'ordre\n    hyperref=true\n]{biblatex} %Imports biblatex package\n\\addbibresource{'+bibfile+'} %Import the bibliography file\n\n\\usepackage{amssymb} %quelques symboles dont gtrsim /lesssim\n\\usepackage{subcaption} % package pour faire des subfigures\n\\usepackage{multirow} % package pour multirow/multicolumn\n\\usepackage{booktabs} % package pour top/mid/bottom rule\n\\usepackage{tcolorbox} % toujours plus de boites\n\\usepackage{xcolor} % Pour avoir des couleurs dans les équations\n\n\\title{}\n\\begin{document}\n'
	return text

def en_tete_complet():
	text="\\documentclass[a4paper, 11pt]{book}\n\n\\usepackage{psl-cover}\n\\usepackage[]{amsmath}\n\\usepackage[]{physics} % \\bra, \\ket etc\n\\usepackage{graphicx} %Pour les figures je crois\n\\usepackage{hyperref}\n\\usepackage[\n    backend=biber, \n    natbib=true,\n    style=numeric-comp,\n    sorting=none, %Pour faire apparaitre les refs dans l'ordre\n    hyperref=true\n]{biblatex} %Imports biblatex package\n\\addbibresource{bib_thesis.bib} %Import the bibliography file\n\n\\usepackage{amssymb} %quelques symboles dont gtrsim /lesssim\n\\usepackage{subcaption} % package pour faire des subfigures\n\\usepackage{multirow} % package pour multirow/multicolumn\n\\usepackage{booktabs} % package pour top/mid/bottom rule\n\\usepackage{tcolorbox} % toujours plus de boites\n\\usepackage{xcolor} % Pour avoir des couleurs dans les équations\n\n\\title{Cross-relaxation in dense ensembles of NV centers and application to magnetometry}\n\n\\author{Clément Pellet-Mary}\n\n\\institute{ENS Paris}\n\\doctoralschool{EDPIF}{564}\n\\specialty{Physique}\n\\date{07 Décembre 2022}\n\n\\jurymember{1}{Dmitry Budker}{Professor JGU Mainz}{Rapporteur}\n\\jurymember{2}{Philippe Tamarat}{Professeur, Université de Bordeaux}{Rapporteur}\n\\jurymember{3}{Maria Chamarro}{Professeure, Sorbonne Université}{Examinateur}\n\\jurymember{4}{Vincent Jacques}{Dirrecteur de recherche, CNRS}{Examinateur}\n\\jurymember{5}{Alexandre Tallaire}{Dirrecteur de recherche, CNRS}{Examinateur}\n\\jurymember{6}{Gabriel Hétet}{Maitre de conférence, ENS Paris}{Directeur de thèse}\n% \\jurymember{9}{Prénom NOM}{Titre, établissement}{Invité}\n% \\jurymember{10}{Prénom NOM}{Titre, établissement}{Invité}\n\n\\frabstract{\nLe centre NV du diamant est un candidat prometteur pour de nombreuses technologies quantiques, que ce soit pour les communications quantiques, le calcul quantique ou la métrologie quantique. Grace aux progrès de synthétisation du diamant, des échantillons contenant une haute concentration en centres NV sont aujourd’hui réalisables. Cette augmentation de la densité de centres NV s’accompagne d’une augmentation des interactions entre ces derniers, ce qui donne lieu à une physique complexe et encore largement inexplorée. De nombreuses applications récentes, telles que l’hyper-polarisation en RMN, la bio-imagerie ou encore la spin-mécanique repose sur des ensembles denses de centres NV. Comprendre et maîtriser les propriétés d’ensemble de ces derniers est un point crucial pour l’établissement de ces technologies.\n\nCette thèse étudie les échanges de polarisation, par relaxation croisée, entre des ensembles denses de centres NV, ainsi que les interactions entre les centres NV et d’autres impuretés paramagnétiques présentes dans le diamant. Le but de ces travaux est de mieux comprendre les propriétés des ensembles de centres NV, et d’exploiter certaines de ces propriétés pour de nouvelles applications telles que la détection d’impuretés ou la magnétométrie.\n\nDans un premier temps, nous détaillerons les propriétés des centres NV et nous introduirons des concepts liés à l’interaction dipolaire entre spins et aux relaxations croisées. Nous verrons ensuite comment les relaxations croisées peuvent être utilisées pour détecter optiquement des résonances de spins qui ne sont pas optiquement actifs, en l’occurrence les défauts VH- et War1 dans des diamants CVD. Enfin nous étudierons les relaxations croisées entre différents sous-groupes de centre NV. Nous verrons d’abord leur influence sur la dynamique du spin et leur origine microscopique, puis nous étudierons leur dépendance avec le champ magnétique et leur potentielle utilisation pour la magnétométrie en champs faible.\n}\n\n\\enabstract{\n  The NV center in diamond is a promising candidate for emerging quantum technologies, including quantum communication, quantum computing and quantum metrology. Thanks to the recent progress in diamond synthesis, samples with high NV center concentration can now be created. This increase in the NV density comes with an increase of the interaction between them, which leads to a rich and complex physics. Numerous applications, such as NMR hyperpolarization, bio-imagery or spin mechanics rely on the use of dense NV ensembles. Understanding and mastering the properties of ensembles of NV centers will be a crucial point in the development of these technologies. \n  \nThis doctoral thesis focuses on cross-relaxation between dense ensembles of NV centers, as well as on the interaction between NV centers and other diamond paramagnetic impurities. The aim of this work is to better understand the properties of dense NV centers ensembles, and to exploit them for new applications such as the detection of impurities and magnetometry. \n\nIn the first part, we will detail the properties of single NV centers and introduce notions regarding dipole-dipole spin coupling and cross-relaxations. We will then show how cross-relaxations can be used to optically detect dark spin resonances, in this case the VH- and War1 defects in CVD-grown diamond. Finally, we will present a study of cross-relaxations between subgroups of NV centers. We will first cover the influence of cross-relaxation on the spin dynamics and discuss its microscopic origin. We will then investigate the role of the magnetic field on cross-relaxations as well as their potential use in low field magnetometry.\n}\n\n\\frkeywords{centre NV, dynamique de spin, magnétométrie}\n\\enkeywords{NV center, spin dynamics, magnetometry}\n\n\\begin{document}\n\n\\maketitle{}\n"
	return text
def closure():
	text='\n\\end{document}\n'
	return text

def addChapter(mainfile,chapterName,chapterDoss):
	f=mainfile
	# f.write('\\begin{refsection}\n')
	file=chapterName
	doss=chapterDoss
	chap=open(file,'r').read()
	chap=chap.split('begin{document}')[1]
	chap=chap.split('\\printbibliography')[0]
	chap=chap.replace('Figures/',doss+'/Figures/')
	f.write(chap)
	# f.write('\\printbibliography')
	# f.write('\n\\end{refsection}\n ')


def fusion_these():
	with open('these_fusion.tex','w') as f:
		f.write(en_tete_complet())
		f.write('\\setcounter{tocdepth}{1}\n')
		f.write('\n\\tableofcontents\n ')

		maintextfiles=['Intro et conclusion/Intro.tex']+['chapter %i/Chapter %i.tex'%(i,i) for i in range(1,5)]+['Intro et conclusion/conclusion.tex']
		maintextdoss=['Intro et conclusion']+['chapter %i'%i for i in range(1,5)]+['Intro et conclusion']

		for i in range(len(maintextfiles)):
			addChapter(f,maintextfiles[i],maintextdoss[i])

		f.write('\n\\appendix\n ')

		appendixFiles=['chapter 1/appendix_samples.tex', 'chapter 3/Appendix_eta.tex','chapter 4/Appendix_autres_causes.tex']
		appendixdoss=['chapter 1', 'chapter 3', 'chapter 4']
		for i in range(len(appendixFiles)):
			addChapter(f,appendixFiles[i],appendixdoss[i])

		f.write('\\printbibliography')
		f.write(closure())

fusion_these()

# with open('sample.tex','r') as f:
# 	print(f.read().__repr__())

