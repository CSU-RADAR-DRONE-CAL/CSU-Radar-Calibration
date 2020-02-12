import tkinter as tk
import numpy as np
import scipy.constants as const

C = const.c
pi = np.pi
#dielectric const of water
Kw = .93
T = .3*10**(-6)
#el_az
fields = ('Transmit Power dBm', 'Range', 'Antenna Gain', 'Reflective Cross Section', 'Transmit Frequency', 'Radar Constant', 'Recieved Power dB')
data = {'kW': .93, 'T':.3*10**(-6), 'C':const.c, 'pi':np.pi}
def received_power(entries):
    r = float(entries['Range'].get())
    print("r", r)
    xmit = 10**((float(entries['Transmit Power dBm'].get())-30)/10)
    print("xmit", xmit)
    Go_squared =  (10**(float(entries['Antenna Gain'].get())/10))**2
    print("Go", Go_squared)
    xsection = float(entries['Reflective Cross Section'].get())
    print("cross section", xsection)
    wavelength_squared = (C/(float(entries['Transmit Frequency'].get())*(10**9)))**2
    print("wavelength_squared", wavelength_squared)
    n = xmit*Go_squared*wavelength_squared*xsection
    d = ((4*pi)**3)*(r**4)
    ans = n/d
    ansdb = 20*np.log10(ans)
    entries['Recieved Power dB'].delete(0, tk.END)
    entries['Recieved Power dB'].insert(0, ansdb)
    print("recieved power: %f" % ansdb)
## TODO: calculate Pr/Prad given antenna constants
##       calculate Z(R)

def rad_const(entries):
    xmit = 10**((float(entries['Transmit Power dBm'].get())-30)/10)
    Go_squared =  Go_squared =  (10**(float(entries['Antenna Gain'].get())/10))**2
    wavelength_squared = (C/(float(entries['Transmit Frequency'].get())*(10**9)))**2
    xsection = float(entries['Reflective Cross Section'].get())
    prdb = float(entries['Recieved Power dB'].get())
    pr = 10**(prdb/10)
    el_azn = xsection*(8*np.log(2)**2)*xmit
    el_azd = (pi**2)*pr*wavelength_squared
    el_az = .0174533**2
    A = (8*np.log(2))/(pi*el_az)
    endterm = wavelength_squared*(10**21)
    ans = (1/((pi**5)*np.abs(Kw)))*(2/(C*T))*((4*(pi**3))/(pr*Go_squared))*A*endterm
    ansdb = 10*np.log10(ans)
    entries['Radar Constant'].delete(0, tk.END)
    entries['Radar Constant'].insert(0, ansdb)
    print("Radar Constant: %f" % ansdb)

def makeform(root, fields):
    entries = {}
    for field in fields:
        print(field)
        row = tk.Frame(root)
        lab = tk.Label(row, width=22, text=field+": ", anchor='w')
        ent = tk.Entry(row)
        ent.insert(0, "0")
        row.pack(side=tk.TOP,
                 fill=tk.X,
                 padx=5,
                 pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT,
                 expand=tk.YES,
                 fill=tk.X)
        entries[field] = ent
    return entries

if __name__ == '__main__':
    root = tk.Tk()
    ents = makeform(root, fields)
    b1 = tk.Button(root, text='Radar Constant',
           command=(lambda e=ents: rad_const(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(root, text='Recieved Power',
           command=(lambda e=ents: received_power(e)))
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    b3 = tk.Button(root, text='Quit', command=root.quit)
    b3.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()
