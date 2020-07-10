import numpy as np
import matplotlib.pyplot as plt

gamma_min=1/200
gamma_max=1/5
gamma_phonon=1/3

def contraste(x):
    return 1-((x+gamma_max+gamma_phonon)*(x+3*(gamma_min+gamma_phonon)))/((x+gamma_min+gamma_phonon)*(x+3*(gamma_max+gamma_phonon)))


absc=np.linspace(0,2,500)

ord=[contraste(x) for x in absc]

plt.plot(absc,ord)
plt.show()