
from chimera import runCommand as rc
from glob import glob

from os import chdir, listdir
chdir(".") 

for m in glob('*.pdb'):
    rc('open ' + m)
    rc("addh")
    rc('write format mol2 0 ' + m[:-4] + '.mol2')
    rc('close all')    
    