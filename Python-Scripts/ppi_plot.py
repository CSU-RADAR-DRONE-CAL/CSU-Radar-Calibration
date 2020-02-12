
import netCDF4
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import matplotlib.colors as colors
from scipy.io import loadmat

cmap_arr = loadmat('/home/straydog/Documents/senior_design/python_scripts/nws.mat')['nwsZ']
fh = Dataset('/home/straydog/Documents/senior_design/netCDF_files/Ku-band/KuD3R_20190328_180759_07.nc')

ndX = (fh.variables['GateWidth'][1])*np.arange(len(fh.dimensions['Gate']))/1000
ndY = fh.variables['Azimuth'][:]
ndY = np.reshape(ndY,(len(fh.variables['Azimuth']),1))*(np.pi/180)
nX = ndX*np.cos(ndY)
nY = ndX*np.sin(ndY)*-1

ncp = fh.variables['NormalizedCoherentPower'][:]
rflct = fh.variables['Reflectivity'][:]

clrs = colors.ListedColormap(cmap_arr, 'reflectivity')
it = np.nditer(ncp, flags=['multi_index'])

while not it.finished:
    x,y = it.multi_index
    if ncp[x][y] < .7:
        rflct[x][y] = np.nan
    it.iternext()

plt.pcolormesh(nY, nX, rflct, vmin = -20, vmax = 64, cmap = clrs)
plt.xlabel('Range (km)')
plt.ylabel('Elevation (m)')
plt.title('RHI reflectivity')
plt.xlim(1000,2500)
plt.ylim(0,500)
plt.colorbar().set_label('dB')
plt.show()
