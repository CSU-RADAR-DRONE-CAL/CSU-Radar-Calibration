import netCDF4
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import matplotlib.colors as colors
import glob
from scipy.io import loadmat
import os
import time
#
#theta,rad = np.meshgrid(used_theta, used_rad) #rectangular plot of polar data
#X = theta
#Y = rad
#
#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.pcolormesh(X, Y, data2D) #X,Y & data2D must all be same dimensions
#plt.show()
cmap_arr = loadmat('nws.mat')['nwsZ']
clrs = colors.ListedColormap(cmap_arr, 'reflectivity')
path = 'csu_rxm25.scvw-20190213-235906.netcdf'

fh = Dataset(path)
gateWidth = fh.variables['GateWidth'][1]
ndX = gateWidth * np.arange(len(fh.dimensions['Gate'])) / 1000
ndY = fh.variables['Azimuth'][:]
vars = fh.variables
varRef = fh.variables['Reflectivity'][:]
varNCP = fh.variables['NormalizedCoherentPower'][:]
varEle = fh.variables['Elevation'][:]
dimGat = len(fh.dimensions['Gate'])
#for i in range(len(varRef)):
#        for j in range(len(varRef[i])):
#            if varNCP[i][j] < 0.7:
#                varRef[i][j] = np.nan
                
elev = fh.variables['Elevation'][14]

ndY = np.reshape(ndY, (len(fh.variables['Azimuth']), 1)) * (np.pi / 180)
nX = ndX * np.cos(ndY)
nY = ndX * np.sin(ndY)
plt.pcolormesh(nY, nX, varRef, vmin=-22, vmax=64, cmap = clrs)
#plt.xlim(-3000, 0)
#plt.ylim(0, 500)
plt.title(elev)
plt.colorbar()
plt.show()
#nY = np.linspace(0,1,len(fh.dimensions['Radial']))
#nX = 59940.95048025*np.linspace(0,1,len(fh.dimensions['Gate']))
##ndY = fh.variables['Azimuth'][:]
#ndY = np.arange(len(fh.dimensions['Radial']))
## TODO: convert nx,ny to polar coordinates
##ndY = np.reshape(ndY,(len(fh.variables['Azimuth']),1))*(np.pi/180)
##nX = ndX*np.cos(ndY)
##nY = ndX*np.sin(ndY)
#X,Y = np.meshgrid(nX,nY)
#r = np.sqrt(X**2+Y**2)
#t = np.radians(np.arctan2(Y,X))
#nX = np.sqrt(ndX**2+ndY**2)
#nY = np.arctan2(ndX,ndY)
#r,t = np.meshgrid(X,Y)
#r = X*np.cos(90-Y)
#t = Y*np.sin(90-Y)
#fig = plt.figure()
#ax = fig.add_subplot(111)#, projection = 'polar')
##plt.pcolormesh(nY, nX, fh.variables['Reflectivity'][:], vmin = -24, vmax = 60, cmap = 'Accent')
##plt.colorbar()
##plt.show()


