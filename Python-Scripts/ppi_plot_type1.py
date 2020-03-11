
import netCDF4
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import matplotlib.colors as colors
from scipy.io import loadmat

cmap_arr = loadmat('/home/straydog/Documents/senior_design/python_scripts/nws.mat')['nwsZ']
fh = Dataset('/home/straydog/Documents/senior_design/netCDF_files/csu_rxm25.scvw-20190213-235906.netcdf')

ndX = (fh.variables['GateWidth'][1])*np.arange(len(fh.dimensions['Gate']))/1000
ndY = fh.variables['Azimuth'][:]
ndY = np.reshape(ndY,(len(fh.variables['Azimuth']),1))*(np.pi/180)
nX = ndX*np.cos(ndY)
nY = ndX*np.sin(ndY)
#print(nY.shape)


#ncp = fh.variables['NormalizedCoherentPower'][:]
rflct = fh.variables['Reflectivity'][:]
print(rflct.shape)
clrs = colors.ListedColormap(cmap_arr, 'reflectivity')
#it = np.nditer(ncp, flags=['multi_index'])

#while not it.finished:
#    x,y = it.multi_index
#    if ncp[x][y] < .7:
#        rflct[x][y] = np.nan
#    it.iternext()

plt.pcolormesh(nY, nX, rflct, vmin = -20, vmax = 64, cmap = clrs)
#plt.xlim(-3000,0)
#plt.ylim(0,500)
#plt.colorbar()
plt.show()
