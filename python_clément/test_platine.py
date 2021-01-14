#La librairie PI se trouve sur https://github.com/git-anonymous/PIPython J'en ai télécargé une version dans le dossier python_clément (à installer avec le setup.py). Pour les exemples j'utilise SimpleMove.py dans sample


from pipython import GCSDevice, pitools

CONTROLLERNAME = 'C-863.11'  # 'C-863' will also work
STAGES = ['M-111.1VG']
REFMODES = ['FNL', 'FRF']

with GCSDevice(CONTROLLERNAME) as pidevice:
	pidevice.ConnectUSB(serialnum='0165500259') #Le serial number il faut aller le chercher dans le logiciel PiMikromove, Quand tu connectes un controller dans USB daisy chain tu devrais voir "PI C-863 Mercury SN 'serial number'"
	print('connected: {}'.format(pidevice.qIDN().strip()))

	pitools.startup(pidevice, stages=STAGES, refmodes=REFMODES)

	rangemin = pidevice.qTMN()
	rangemax = pidevice.qTMX()
	curpos = pidevice.qPOS()

	print(rangemin,rangemax,curpos)

	axis=1
	target=15 #en mm min=0 max=15
	velocity=0.6 #en mm/s max=0.65

	pidevice.VEL(axis,velocity)
	print(pidevice.qVEL(axes=axis))	
	pidevice.MOV(axis,target)
	while not pidevice.qONT(axes=axis)[1] :
	 	pass
	print('finito')
	# pitools.waitontarget(pidevice, axes=axis)

