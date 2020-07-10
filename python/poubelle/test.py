import numpy as np
import matplotlib.pyplot as plt

gamma_min=1
gamma_max=5

def contraste(x):
    return 1-((x+gamma_max)*(x+3*gamma_min))/((x+gamma_min)*(x+3*gamma_max))


absc=np.linspace(0,20,500)

ord=[contraste(x) for x in absc]

plt.plot(absc,ord)
plt.show()