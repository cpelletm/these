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
returned_value = os.system(cmd)  # returns the exit code in unix

cmd='cpelletm'
returned_value = os.system(cmd)  # returns the exit code in unix

cmd='monmdpgithubunpeuplussafe' #moyennement safe du coup
returned_value = os.system(cmd)  # returns the exit code in unix