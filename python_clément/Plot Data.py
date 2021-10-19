from lab import *
from analyse import *



def choseFileAction():
	import csv
	lineSelection.removeAll()
	global startPath
	filename,filters=QFileDialog.getOpenFileName(directory=startPath,filter='*.csv')
	if filename :	
		startPath=os.path.dirname(filename)
		with open(filename,'r',encoding = "ISO-8859-1") as f:
			global data
			data = list(csv.reader(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_NONNUMERIC))
		for i in range(len(data)//2):
			lineSelection.addItem('Line %i'%(i+1))
		lineSelection.setEnabled(True)

def choseLineAction():
	i=lineSelection.index()
	global x,y
	x=data[2*i]
	y=data[2*i+1]
	gra.updateLine(l1,x,y)
	endSelect.setValue(len(x))
	beginSelect.setEnabled(True)
	endSelect.setEnabled(True)

def changeWindowAction():
	try :
		gra.updateLine(l1,x[val(beginSelect):val(endSelect)],y[val(beginSelect):val(endSelect)])
	except Exception as error :		
		tb=traceback.extract_tb(error.__traceback__)
		print(error)
		print(''.join(tb.format()))
		warningGUI('Could not plot the selected window (min=0,max=%i)'%len(x))


startPath=defaultDataPath

choseFile=button('Chose File',action=choseFileAction,spaceAbove=0)
lineSelection=dropDownMenu('Chose Line',spaceAbove=0, action=choseLineAction)
lineSelection.setEnabled(False)
beginSelect=field('From',0,spaceAbove=0,action=changeWindowAction)
beginSelect.setEnabled(False)
endSelect=field('To',100,spaceAbove=0,spaceBelow=1,action=changeWindowAction)
endSelect.setEnabled(False)
# Hbox=box(beginSelect,endSelect,spaceBelow=1)

leftFields=[choseFile,lineSelection,beginSelect,endSelect]

gra=graphics()
l1=gra.addLine()


trace=keepTraceButton(l1,spaceBelow=1)
norm=gra.normalize()
norm.setState(False)
rightFields=[norm,trace]

GUI=Graphical_interface(leftFields,gra,rightFields,title='Plot Data')
GUI.run()