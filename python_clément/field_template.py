class field_template():
	def __init__(self):

		#creation
		self.labeldummy=QLabel("dummy")
		self.lectdummy=QLineEdit(str(self.dummy))
		Vbox_gauche.addWidget(self.labeldummy)
		Vbox_gauche.addWidget(self.lectdummy)
		Vbox_gauche.addStretch(1)

		#lecture /!\ float/int
		self.dummy=np.int(self.lectdummy.text())