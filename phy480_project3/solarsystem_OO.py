# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 19:12:49 2017

@author: samme
"""
import numpy as np
import matplotlib.pyplot as plt
import planetclass as pc
import matplotlib.animation as animation
tempG = 6.67*10**(-11); # unmolested gravitational constant
yr = 365*60*60*24; # number of seconds in a year
B = 5.972*10**24; # mass of the earth in kg
AU = 1.496*10**11; # 1 AU in meters
Ms = 332946.0487 # mass of the sun in units of mass of the earth
GMs = 4*np.pi**2 * AU**3 / yr**2

names = ['sun','mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']

def distance(P1, P2):
    '''
    distance(P1, P2) will determine the radius and vectorized distance between two planets
    the separation vector will point from P1 to P2
    '''
    pos1 = P1
    pos2 = P2
    separation = pos2 - pos1
    radius = np.dot(separation,separation)**0.5
    return radius, separation
    
# this is also the force in units of AU, M(earth), years. Thus the acc of the earth takes the same form since Me == 1
def acc(P1,P2,mass1):
    '''
    the sep vector points from P1 to P2. Thus we want the planet of interest to be input as P2, 
    this way the sep vec points from say, the sun to the earth
    '''
    r,sep = distance(P1,P2)
    x,y,z = sep
    ax = x / (r)**3
    ay = y / (r)**3
    az = z / (r)**3
    output = -np.array([ax,ay,az]) * 4*np.pi**2 * mass1 / Ms
    return output  
    

def load_data(planet_name):
    fout = 'planet_' + planet_name
    data = np.loadtxt(fout)
    x = data[:,0]
    y = data[:,1]
    z = data[:,2]
    E = data[:,3]
    L = data[:,4]
    return x,y,z,E,L
    
def make_planets(model = 'verlet'):
    if type(model) == str:
        pass
    elif model in range(['verlet','euler']):
        pass
    else:
        print('please enter the model as a string')
        input('verlet or euler: ')
    mass = [Ms,.06, .82, 1, .11, 317.8, 95.2, 14.6, 17.2] #w.r.t earth mass
    location = [np.array([3.05*10**(-3),4.63*10**(-3),-1.49*10**(-4)]),
                np.array([-.391,-.107,.0269]),
                np.array([-.555,-.455,.0257]),
                np.array([-.899,-.435,-1.29*10**(-4)]),
                np.array([.396,1.49,.0212]),
                np.array([-5.17,-1.74,.123]),
                np.array([-1.32,-9.96,.226]),
                np.array([18.2,8.19,-.205]),
                np.array([28.4,-9.38,-.462])]
    velocity = [np.array([3.73*10**-6,-6.49*10**-6,-8.37*10**-8]),
                np.array([1.82*10**-3,-2.59*10**-2,-2.28*10**-3]),
                np.array([1.27*10**-2,-1.57*10**-2,-9.49*10**-4]),
                np.array([7.24*10**-3,-1.55*10**-2,8.64*10**-7]),
                np.array([-1.30*10**-2,4.79*10**-3,4.19*10**-4]),
                np.array([2.32*10**-3,-6.79*10**-3,-2.36*10**-5]),
                np.array([5.23*10**-3,-7.50*10**-4,-1.95*10**-4]),
                np.array([-1.64*10**-3,3.40*10**-3,3.38*10**-5]),
                np.array([9.62*10**-4,3.00*10**-3,-8.38*10**-5])] #in AU/day
    period = [0,.24,.62,1,1.88,11.86,29.46,84.01,164.8] #years   
    planets = []
    sun_vel = np.array([0.0,0.0,0.0])
    for jj in np.arange(len(names)-1):
        sun_vel += mass[jj+1] * velocity[jj+1] * 365

    for i in np.arange(0,len(names)):
        planets.append(pc.planet(names[i]))
        planets[i].mass = mass[i]
        planets[i].pos = location[i]
        planets[i].vel = velocity[i] * 365
    return planets
    
def centerofmass():
    mass = [Ms,.06, .82, 1, .11, 317.8, 95.2, 14.6, 17.2]
    datasun = load_data('sun')
    cm = np.zeros((3,len(datasun[0])))
    for i in np.arange(len(mass)):
        data = load_data(names[i])
        
        x = data[0] - datasun[0]
        y = data[1] - datasun[1]
        z = data[2] - datasun[2]
        pmass = mass[i]
        xcm = x * pmass
        ycm = y * pmass
        zcm = z * pmass
        cm +=np.array([xcm,ycm,zcm])
    cm = cm/np.sum(mass)
    
    sunradius = 0.00464913034 #AU
    circle = np.zeros((2,len(datasun[0])))
    angle = np.linspace(0,2*np.pi,len(x))
    for i in np.arange(len(x)):
        circle[:,i] = np.array([sunradius*np.cos(angle[i]),sunradius*np.sin(angle[i])])
        
    fig = plt.figure('center of mass')
    plt.plot(cm[0],cm[1],label='Center of Mass',lw=2)
    plt.hold(True)
    plt.plot(circle[0],circle[1],label='Radius of Sun', lw=20)
    plt.xlabel('x-axis [AU]')
    plt.ylabel('y-axis [AU]')
    plt.legend()
    plt.show()
    
def acc_update(planet_list,planet='all'):
    planets = planet_list
    accel = 0
    accell = 0
    PE = 0
    if planet=='all':
        for i in np.arange(len(planets)):
            for j in np.arange(len(planets)):
                if i == j:
                    continue
                else:
                    accel += acc(planets[j].pos,planets[i].pos, planets[j].mass)
                    PE += np.abs(np.dot(accel,accel) * planets[i].mass * distance(planets[j].pos,planets[i].pos)[0])
            planets[i].PE = PE
            planets[i].acc = accel
    else:
        for i in np.arange(len(planets)):
            if planets[i].name == planet:
                place = i
            else:
                continue
        for j in np.arange(len(planets)):
            if j == place:
                continue
            else:
                accell += acc(planets[j].pos,planets[place].pos,planets[j].mass)
                PE += np.abs((np.dot(accell,accell))**(.5) * planets[place].mass * distance(planets[j].pos,planets[place].pos)[0])
        planets[place].PE = PE
        planets[place].acc = accell

def plot(figure = 'orbits'):
    planets = names
    datasun = load_data('sun')
    for i in np.arange(len(planets)):
        data = load_data(planets[i])
        angmo = np.array([0.0,0.0,0.0])
        if figure == 'orbits':
            from mpl_toolkits.mplot3d import Axes3D
            orbits = plt.figure('orbits')
            #ax = orbits.add_subplot(111, projection='3d')
            #ax.scatter(data[0]-datasun[0],data[1]-datasun[1],data[2]-datasun[2],label=planets[i])
            plt.plot(data[0]-datasun[0],data[1]-datasun[1],label=planets[i],lw=2)
            plt.hold(True)
            plt.xlim([-31,31])
            plt.ylim([-31,31])
            plt.xlabel('x-pos [AU]')
            plt.ylabel('y-pos [AU]')
            plt.legend(fontsize=36)
    
        elif figure == 'energy':
            energy = plt.figure('energy')
            '''
            if i in [0,5,6]:
                energy.add_subplot(212)
                plt.plot(data[3],label=planets[i],lw=2)
            else:
                energy.add_subplot(211)
                plt.plot(data[3],label=planets[i],lw=2)
            '''
            plt.plot(data[3],label=planets[i],lw=2)
            plt.hold(True)
            plt.ylabel('total energy [a.u.]')
            plt.legend(fontsize=36)
    
        elif figure =='angularmo':
            angular_mo = plt.figure('angular momentum')
            if i in [0]:
                continue
            else:
                plt.plot(data[4],label=planets[i],lw=2)
            
            #plt.plot(data[4]/np.max(data[4]),label=planets[i],lw=2)
            plt.hold(True)
            plt.ylabel('Angular Momentum [a.u.]')
            plt.legend(fontsize=36)
 
    
def ssverlet(V0 = 2*np.pi, years = 1):
    N = 365 * years
    dt = 1/365
    planets = make_planets()
    acc_update(planets)
    for t in np.arange(N):
        for i in np.arange(len(planets)):
            planets[i].update()
            planets[i].pos = planets[i].pos_old + planets[i].vel_old * dt + 1/2 * dt**2 * planets[i].acc_old - planets[0].pos
            acc_update(planets,planet=planets[i].name)
            planets[i].vel = planets[i].vel_old + 1/2*(planets[i].acc_old + planets[i].acc) * dt - planets[0].vel
            if (t % N/10) % 1 == 0:
                planets[i].output()
            else:
                pass    

def plotmov():
    fig = plt.figure('animate')
    ax = fig.add_subplot(111,aspect='equal',autoscale_on=False,xlim=(-31,31), ylim=(-31,31))
    planets = make_planets()
    x = []
    y = []
    z = []
    for i in np.arange(len(planets)):
        x0,y0,z0 = load_data(planets[i].name)
        x.append(x0)
        y.append(y0)
        z.append(z0)
    elements = int(len(x0)/20)
    lines = []
    line, = ax.plot([],[], label = 'sun')
    '''
    def animate(i):
        lines[0].set_data(x0[:i],y0[:i])
        return line,
    def init():
        line.set_data([],[])
        return line,
    '''
    for i in np.arange(0):
        lines.append([])
        lineobj, = ax.plot([],[],lw=2, label=planets[i].name)
        lines.append(lineobj,)
        
    def animate(i):
        place = 0
        for line in lines:
            line.set_data(x[place,:i],y[place,:i])
            place += 1
        return tuple(lines)
    
    
    # Init only required for blitting to give a clean slate.
    def init():
        for line in lines:
            line.set_data([],[])
        return lines
    
    ax.legend()
    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=100, interval=20, blit=True)
    ani.save('orbitss.mp4')
    plt.show()
