"""
Demo of automatically generating a 3D-printable STL WRL file from a SWC file.
from mpi4py import MPI
COMM = MPI.COMM_WORLD
SIZE = COMM.Get_size()
RANK = COMM.Get_rank()
"""
from distributed import dask
from neuron import h
from prepare_3dprintable import ctng
from mayavi import mlab
import sys
sys.path.append('geometry3d')
from surface import surface
from triangularMesh import TriangularMesh
from voxelize import voxelize
from scalarField import ScalarField

import os
os.system('ls *.swc > swc_names.txt')
f = open('swc_names.txt')
nfs = [line.strip() for line in open('swc_names.txt', 'r')]
f.close()

h.load_file('stdlib.hoc')
h.load_file('import3d.hoc')
itergids = iter([i for i in nfs])

def func2map(i):
    cell = h.Import3d_SWC_read()
    print(len(nfs))
    print(i)
    morphology_filename = nfs[i]
    cell = h.Import3d_SWC_read()
    cell.input(morphology_filename)
    i3d = h.Import3d_GUI(cell, 0)
    i3d.instantiate(None)
    file_name=str(nfs[i])+str('.wrl')
    print(file_name)
    ctng(show=False, magnification=200,file_name=file_name)
    mlab.savefig(str(nfs[i])+'.wrl')
'''
TODO make this work
from dask.distributed import Client
futures = client.map(func2map, itergids)
results = await client.gather(futures, asynchronous=True)
return results
'''
futures = map(func2map,itergids)
import os
os.system('ls *.wrl > wrl_names.txt')
f = open('wrl_names.txt')
wrl = [line.strip() for line in open('wrl_names.txt', 'r')]
f.close()

for f in wrl:
    exec_string = './meshconv '+str(f)+'-c stl'
    os.system(exec_string)
