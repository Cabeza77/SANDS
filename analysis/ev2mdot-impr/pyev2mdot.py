#!/usr/bin/python3

import os
import re
import numpy as np
import sys


def ev2mdot(simname, sinknumber, period, bins, periodave):

    ''' 
    
    three main parameters: orbit time, orbit bins, orbits to average onto
    
    import .ev data in numpy array
    
    average and return the result
    
    '''
    
    evfiles=[ev for ev in sorted(os.listdir('./')) if (re.search('^'+simname+'Sink'+str(sinknumber).zfill(4)+'N', ev) and re.search('.ev$', ev))]
    
    datain=np.concatenate([np.loadtxt('./'+ev, unpack=False, skiprows=1) for ev in evfiles], axis=0)
        
    dataout=[[0,0,0]]
    dataoutave=[]
    
    tm_prev=0
    tm_in=0
    tm_in_av=0
    j_in=1
    macc=0
    
    #print(datain[0:10])
    
    for tmstep in datain:
        if tmstep[0]<=tm_prev:
            continue
        
        if (tmstep[0])%(period/bins)<tm_prev%(period/bins):
            dataout.append([tmstep[0],
                            (tmstep[11]-macc)/(tmstep[0]-tm_in),
                            tmstep[11]-macc])
            tm_in=tmstep[0]
            macc=tmstep[11]
            
            if (len(dataout)-1)%(bins*periodave)==0:
                for i in range(0, bins):
                    j=i+j_in
                    
                    dataoutave.append(
                        [dataout[-bins+i][0],
                         np.sum(np.array(dataout)[j::bins,2])/np.sum(np.array(dataout)[j::bins,0]-np.array(dataout)[j-1:-1:bins,0]),
                         #np.mean(np.array(dataout)[j::bins,2])])
                         np.sum(np.array(dataout)[j::bins,2])])
                    
                j_in+=periodave*bins
                tm_in_av=tmstep[0]
                    
                    
                    
        tm_prev=tmstep[0]
        prev_line=tmstep
                    
    return np.array(dataoutave)

if __name__=="__main__":
    simname='GGT106-visc'
    sinknumber=1
    
    period=1030.91252 #0.341713895
    bins=2
    periodave=10

    if len(sys.argv)==6:
        simname=sys.argv[1] # 'GGT106-visc'
        sinknumber=int(sys.argv[2]) # 1
        
        period=float(sys.argv[3]) # 1030.91252 #0.341713895
        bins=int(sys.argv[4]) # 2
        periodave=int(sys.argv[5]) # 10
    else:
        print('Usage: ',sys.argv[0],'simname sinknumber period bins average-over')
        sys.exit(1)

    
    print('#time','mdot','accr_mass', sep='\t\t\t\t')
    for line in ev2mdot(simname, sinknumber, period, bins, periodave):
        print(line[0], line[1], line[2], sep='\t\t')
    #print(ev2mdot(simname, sinknumber, period, bins, periodave))
