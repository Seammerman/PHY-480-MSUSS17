# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 19:12:49 2017

@author: samme
"""
import numpy as np
import matplotlib.pyplot as plt

tempG = 6.67*10**(-11); # unmolested gravitational constant
yr = 365*60*60*24; # number of seconds in a year
B = 5.972*10**24; # mass of the earth in kg
AU = 1.496*10**11; # 1 AU in meters
Ms = 332946.0487 # mass of the sun in units of mass of the earth
G = tempG * B * A**2 / C
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
    ax = x /(x**2 + y**2)**(3/2)
    ay = y /(x**2 + y**2)**(3/2)
    output = -np.array([ax,ay]) * 4*np.pi**2
    return output

    
    
    
    
def euler(V0 = 2*np.pi):
    years = 10
    N = 365 * years
    dt = 1/365
    Pearth = np.array([1,0])
    Vearth = np.array([0,V0])
    pos_vec = np.zeros((N,2))
    vel_vec = np.zeros((N,2))
    acc_vec = np.zeros((N,2))
    vel_vec[0,:] = Vearth
    pos_vec[0,:] = Pearth
    acc_vec[0,:] = acc(Pearth)
    for i in np.arange(0,N-1):
        pos_vec[i+1,:] = pos_vec[i,:] + vel_vec[i,:] * dt
        vel_vec[i+1,:] = vel_vec[i,:] + acc(pos_vec[i,:]) * dt
        acc_vec[i+1,:] = acc(pos_vec[i+1,:])
    plt.figure('Euler Method')
    plt.ylim([-3,3])
    plt.xlim([-3,3])
    plt.plot(pos_vec[:,0],pos_vec[:,1])
    plt.xlabel('x-pos [AU]')
    plt.ylabel('y-pos [AU]')
    plt.title('Earth Orbit under Eurler Integration')
    plt.show()
    return
    
def verlet(V0 = 2*np.pi):
    years = 10
    N = 365 * years
    dt = 1/365
    Pearth = np.array([1,0])
    Vearth = np.array([0,V0])
    pos_vec = np.zeros((N,2))
    vel_vec = np.zeros((N,2))
    acc_vec = np.zeros((N,2))
    vel_vec[0,:] = Vearth
    pos_vec[0,:] = Pearth
    acc_vec[0,:] = acc(Pearth)
    for i in np.arange(0,N-1):
        pos_vec[i+1,:] = pos_vec[i,:] + vel_vec[i,:] * dt + 1/2 * dt**2 * acc(pos_vec[i,:])
        vel_vec[i+1,:] = vel_vec[i,:] + 1/2*(acc(pos_vec[i,:]) + acc(pos_vec[i+1,:])) * dt
        acc_vec[i+1,:] = acc(pos_vec[i+1,:])
    plt.figure('Verlet Method')
    plt.ylim([-1,1])
    plt.xlim([-1,1])
    plt.plot(pos_vec[:,0],pos_vec[:,1])
    plt.xlabel('x-pos [AU]')
    plt.ylabel('y-pos [AU]')
    plt.title('Earth Orbit under Verlet Integration')
    plt.show()
    return
