# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 19:12:49 2017

@author: samme
"""
import numpy as np
import matplotlib.pyplot as plt
import planetclass as pc

tempG = 6.67*10**(-11); # unmolested gravitational constant
yr = 365*60*60*24; # number of seconds in a year
B = 5.972*10**24; # mass of the earth in kg
AU = 1.496*10**11; # 1 AU in meters
Ms = 332946.0487 # mass of the sun in units of mass of the earth
GMs = 4*np.pi**2 * AU**3 / yr**2

def distance(Pearth, Psun):
    pos1 = Pearth
    pos2 = Psun
    separation = pos2 - pos1
    radius = np.dot(separation,separation)**0.5
    return radius, separation
    
# this is also the force in units of AU, M(earth), years. Thus the acc of the earth takes the same form since Me == 1
def acc(Pearth):
    x = Pearth[0]
    y = Pearth[1]
    z = Pearth[2]
    r = (x**2 + y**2 + z**2)**(1/2)
    ax = x / (r)**3
    ay = y / (r)**3
    az = z / (r)**3
    output = -np.array([ax,ay,az]) * 4*np.pi**2
    return output  
    

def load_data(planet_name):
    fout = 'planet_' + planet_name
    data = np.loadtxt(fout)
    x = data[:,0]
    y = data[:,1]
    z = data[:,2]
    return x,y,z
    
def euler(V0 = 2*np.pi):
    years = 10
    N = 365 * years
    dt = 1/365
    Earth = pc.planet('earth_euler',1,np.array([1,0,0]),np.array([0,V0,0]))
    Earth.acc = acc(Earth.pos)
    for i in np.arange(0,N-1):
        Earth.update()
        Earth.pos = Earth.pos_old + Earth.vel_old * dt
        Earth.vel = Earth.vel_old + Earth.acc_old * dt
        Earth.acc = acc(Earth.pos)
        if (i % N/10) % 1 == 0:
            Earth.output()
        else:
            pass
        
    #load data that was output just above
    x,y,z = load_data(Earth.name)
    
    plt.figure('Euler Method')
    plt.ylim([-3,3])
    plt.xlim([-3,3])
    plt.plot(x,y)
    plt.xlabel('x-pos [AU]')
    plt.ylabel('y-pos [AU]')
    plt.title('Earth Orbit under Eurler Integration')
    plt.show()
    return
    
def verlet(V0 = 2*np.pi):
    years = 10
    N = 365 * years
    dt = 1/365
    Earth = pc.planet()
    Earth.name = 'earth_verlet'
    Earth.pos = np.array([1,0,0])
    Earth.mass = 1
    Earth.vel = np.array([0,V0,0])
    Earth.acc = acc(Earth.pos)
    for i in np.arange(0,N-1):
        Earth.update()
        Earth.pos = Earth.pos_old + Earth.vel_old * dt + 1/2 * dt**2 * Earth.acc_old
        Earth.acc = acc(Earth.pos)
        Earth.vel = Earth.vel_old + 1/2*(Earth.acc_old + Earth.acc) * dt
        if (i % N/years) % 1 == 0:
            Earth.output()
        else:
            pass
    
    #load calculations
    x,y,z = load_data(Earth.name)
    print(len(z))
    plt.figure('Verlet Method')
    plt.ylim([-1,1])
    plt.xlim([-1,1])
    plt.plot(x,y)
    plt.xlabel('x-pos [AU]')
    plt.ylabel('y-pos [AU]')
    plt.title('Earth Orbit under Verlet Integration')
    plt.show()
    return
