import os
from datetime import date

cmd='cd ~/these'
returned_value = os.system(cmd)  # returns the exit code in unix

cmd='git pull'
returned_value = os.system(cmd)  # returns the exit code in unix

cmd='git add *'
returned_value = os.system(cmd)  # returns the exit code in unix

cmd='git commit -m ordibureau'+str(date.today())
returned_value = os.system(cmd)  # returns the exit code in unix

cmd='git push'
with os.popen(cmd,'w') as p :  # returns the exit code in unix
	p.write('cpelletm')
	p.write('monmdpgithubunpeuplussafe')
