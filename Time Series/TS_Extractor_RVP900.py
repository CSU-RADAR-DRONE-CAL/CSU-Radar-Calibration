"""
RVP 900 Timeseries data extractor

Last edited on 2019/09/03

@author: Shashank Joshil, Colorado State University
"""
from __future__ import print_function
import sys
import struct
import numpy as np
import scipy.io as si

def print_Usage_and_Exit():
    
    print("Usage: testing.py file_name, outpath")
    
    sys.exit(-1)

def parse_pd(pd):
    ih = pd[0:len(pd)//2:2]
    qh = pd[1:len(pd)//2:2]
    iv = pd[len(pd)//2::2]
    qv = pd[len(pd)//2+1::2]
    return ih, qh, iv, qv

def parse_ph(ph):
    c_list = []
    v_list = []
    for i in range(1, len(ph)-1):
        [content, value]= ph[i].decode('ascii').split("=")
        c_list.append((content, 'O'))
        v_list.append([value[:-1]])
    return c_list, tuple(v_list)
    
def parse_pi(pi):
    c_list = []
    v_list = []
    for i in range(1, len(pi)-1):
        [content, value]= pi[i].decode('ascii').split("=")
        c_list.append((content, 'O'))
        v_list.append([value[:-1]])
    return c_list, tuple(v_list)
    
def read_rvptsPulseInfo(fp):
    
    info_data = list()
    
    while True:
        
        line = fp.readline()
        
        if line == b'':
            
            return -1
        
        info_data.append(line)
        
        if line[:18] == b'rvptsPulseInfo end':
            
            break
        
    return info_data
        
        
        
def read_rvptsPulseHead(fp):
    
    head_data = list()
    
    while True:
        
        line = fp.readline()
        
        if line == b'':
            
            return -1
        
        head_data.append(line)
        
        if line[:17] == b'rvptsPulseHdr end':	
            break
   
    return head_data
        
def rvpts_decipher(word):
    
    number = struct.unpack("H", word)[0]
     
    if number & 0xf000 :
        
        iMan = int(number & 0x7ff)
        
        iExp = int((number >> 12) & 0x00f)
        
        if (number & 0x0800):
            
            iMan |= 0xfffff000
            
        else:
            
            iMan |= 0x00000800
            
        if (iMan & 0x80000000):
            
            iMan = - ((iMan ^ 0xffffffff) + 1)
            
        fl32 = float(iMan) * float(int(1 << iExp)) / 3.3554432E7
        
    else:
        
        r = int(number << 20)

        if (r & 0x80000000):
            
            r = - ((r ^ 0xffffffff) + 1)        
        
        fl32 = float(r) / 1.759218603E13
        
    return fl32
        
def read_rvptsPulseData(fp,value_send):
    
    data = list()
    
    data_length = value_send * 8
	
    data_chuck = fp.read(data_length)
    
    if len(data_chuck) < data_length:
        
        return -1
    
    for i in range(int(data_length/2)):
        
        word = data_chuck[i*2:i*2+2]
        
        fl32 = rvpts_decipher(word)
        
        data.append(fl32)
        
    return data
        
        
        
    
def read_file(fp, path, num):

    print('start')
    
    idata = read_rvptsPulseInfo(fp)
    
    if idata == -1:
        
        sys.exit(-1)
    
    ci, li = parse_pi(idata)
    #print(ci)
    #print(li)
    #print(type(ci))    
    #print(np.dtype(ci))
    di = np.dtype(ci)
    
    out_data = {}
        
    out_data['pulse_info'] = np.array([li], dtype = di).reshape(1, 1)
    
    pulse_count = 0
    
    lh_list = []
    
    ih_l = []
    
    qh_l = []
    
    iv_l = []
    
    qv_l = []
    
    while pulse_count <= 10000000000:
        
        hdata = read_rvptsPulseHead(fp)
        
        if hdata == -1:
            
            break
        
        value_str = hdata[21]
        value_send = int(value_str[9:13])
        print(value_send)	
        [ch, lh] = parse_ph(hdata)
        
        lh_list.append(lh)
    
        data = read_rvptsPulseData(fp,value_send)
        
        if data == -1:
            
            break
        
        pulse_count += 1
        
        ih, qh, iv, qv= parse_pd(data)
        
        ih_l.append(ih)
        
        qh_l.append(qh)
        
        iv_l.append(iv)
        
        qv_l.append(qv)

        if pulse_count % (num/10) == 0:
            
            print('=', end='', flush=True)
        
        if pulse_count % num == 0:
            
            print(pulse_count)
        
            dh = np.dtype(ch)
        
            out_data['header_info'] = np.array([lh_list], dtype = dh)

            out_data['HI'] = np.array(ih_l)

            out_data['HQ'] = np.array(qh_l)

            out_data['VI'] = np.array(iv_l)

            out_data['VQ'] = np.array(qv_l)
            
            # path =  '/net/denali/storage2/radar2/tmp/sjoshil/Converter_timeseries/test/result' + str(pulse_count) + '.mat'

            outpath =  path + '/' + str(pulse_count) + '.mat'
            
            si.savemat(outpath, out_data)
            
            lh_list = []
    
            ih_l = []
    
            qh_l = []
    
            iv_l = []
    
            qv_l = []      
    
    dh = np.dtype(ch)
        
    out_data['header_info'] = np.array([lh_list], dtype = dh)
    
    out_data['HI'] = np.array(ih_l)
    
    out_data['HQ'] = np.array(qh_l)
    
    out_data['VI'] = np.array(iv_l)
    
    out_data['VQ'] = np.array(qv_l)
        
    outpath =  path + '/' + str(pulse_count) + '.mat'
            
    si.savemat(outpath, out_data)

    print('finish')
    
    return 0
        
    
    
    
    
def main(arg=None):

    if len(sys.argv) != 4:
        
        print_Usage_and_Exit()
        
    infile = sys.argv[1]

    path = sys.argv[2]

    num = int(sys.argv[3])
    
    fp = open(infile, "rb")
    
    read_file(fp, path, num)
    
    fp.close()
    

if __name__ == '__main__':
    main()
