from lab import *
from analyse import *



def choseFileAction(filename=False):
	import csv
	lineSelection.removeAll()
	global startPath,lastFile
	if not filename :
		filename,filters=QFileDialog.getOpenFileName(directory=startPath,filter='*.csv')
	GUI.changeTitle('Plot Data:'+filename)
	lastFile=filename
	if filename :	
		startPath=os.path.dirname(filename)
		with open(filename,'r',encoding = "ISO-8859-1") as f:
			global data
			data = list(csv.reader(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_NONNUMERIC))
		for i in range(len(data)//2):
			lineSelection.addItem('Line %i'%(i+1))
		lineSelection.setEnabled(True)
		try :
			assert lastIndex < len(lineSelection.dic) #Sinon il est trop malin et il plante pas
			lineSelection.setIndex(lastIndex)
			choseLineAction()
		except :
			lineSelection.setIndex(0)
			choseLineAction()

def choseLineAction():
	i=lineSelection.index()
	global x,y,lastIndex
	lastIndex=i
	x=data[2*i]
	y=data[2*i+1]
	gra.updateLine(l1,x,y)
	endSelect.setValue(len(x))
	beginSelect.setEnabled(True)
	endSelect.setEnabled(True)

def changeWindowAction():
	try :
		gra.updateLine(l1,x[val(beginSelect):val(endSelect)],y[val(beginSelect):val(endSelect)])
	except :		
		warningGUI('Could not plot the selected window (min=0,max=%i)'%len(x))

def keyPressed(e):
	if e.key()==Qt.Key_Up :
		pass
	elif e.key()==Qt.Key_Down :
		pass
	elif e.key()==Qt.Key_Left :
		try :
			folder=os.path.dirname(lastFile)
			try :
				fnames,fval=extract_glob(SubFolderName=folder)
			except :
				fnames=sorted(glob.glob(folder+'/*.csv'))
			i=fnames.index(lastFile)
			if i >0 :
				newFile=fnames[i-1]
				choseFileAction(newFile)
		except :
			print ('failed')
	elif e.key()==Qt.Key_Right :
		try :
			folder=os.path.dirname(lastFile)
			try :
				fnames,fval=extract_glob(SubFolderName=folder)
			except :
				fnames=sorted(glob.glob(folder+'/*.csv'))
			i=fnames.index(lastFile)
			if i<len(fnames)-1 :
				newFile=fnames[i+1]
				choseFileAction(newFile)
		except :
			print ('failed')
	else :
		return

startPath=defaultDataPath

choseFile=button('Chose File',action=choseFileAction,spaceAbove=0)
lineSelection=dropDownMenu('Chose Line',spaceAbove=0, action=choseLineAction, actionType='activated')
lineSelection.setEnabled(False)
beginSelect=field('From',0,spaceAbove=0,action=changeWindowAction)
beginSelect.setEnabled(False)
endSelect=field('To',100,spaceAbove=0,spaceBelow=1,action=changeWindowAction)
endSelect.setEnabled(False)
# Hbox=box(beginSelect,endSelect,spaceBelow=1)

leftFields=[choseFile,lineSelection,beginSelect,endSelect]

gra=graphics()
l1=gra.addLine()

fit=fitButton(l1,menu=True)
trace=keepTraceButton(l1,spaceBelow=1)
norm=gra.normalize()
norm.setState(False)
rightFields=[norm,fit,trace]

global GUI
GUI=Graphical_interface(leftFields,gra,rightFields,title='Plot Data',keyPressed=keyPressed)
GUI.run()