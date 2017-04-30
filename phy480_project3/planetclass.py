# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 17:39:13 2017

@author: samme
"""
import numpy as np

class planet():
    def __init__(self,name):
        self.mass = 0
        self.name = name
        self.pos = np.array([0,0,0])
        self.pos_old = np.array([0,0,0])
        
        self.vel = np.array([0,0,0])
        self.vel_old = np.array([0,0,0])
        
        self.acc = np.array([0,0,0])
        self.acc_old = np.array([0,0,0])
        
        self.KE = 0
        self.PE = 0
        self.L = np.array([0,0,0])
        open('planet_' + self.name, 'w+').close
    def kinetic_energy(self):
        self.KE = 1/2 * self.mass * np.dot(self.vel,self.vel)
        
    def angular_mo(self):
        self.L = np.cross(self.pos,self.mass*self.vel)
        
    def output(self):
        x = self.pos[0]
        y = self.pos[1]
        z = self.pos[2]
        self.kinetic_energy()
        self.angular_mo()
        E = self.KE - self.PE
        l = self.L
        L = np.dot(l,l)
        
        datafile = open('planet_' + self.name, 'a')
        s = "{0} {1} {2} {3} {4}\n".format(x,y,z,E,L)
        datafile.write(s)
        datafile.close()

    def update(self):
        self.pos_old = self.pos
        self.vel_old = self.vel
        self.acc_old = self.acc