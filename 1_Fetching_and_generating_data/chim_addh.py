
from chimera import runCommand as rc

from os import chdir, listdir
chdir("../../ARCHIVOS/CRISTALES/LIGS_ERK2/POCKET_LIGS/") 

for m in listdir('.'):
    rc('open ' + m)
    rc("addh")
    rc('write format mol2 0 ' + m[:-4] + '.mol2')
    rc('close all')    
    