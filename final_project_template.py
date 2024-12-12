#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 06:54:12 2024

@author: keiragupta
"""

import numpy as np
import matplotlib.pyplot as plt
"""
PART 2
"""
### INITIAL CONDITIONS
# Setting up the spatial grid
dx = 20 #m
x = np.arange(0, 5001, dx) #m
nodes = len(x)

# Setting up the initial concentration of silver iodide
# In this scenario, the silver iodide is sprayed once with a concentration of 10e-7, and travels 60m starting at x = 40m.

c = np.zeros(nodes)
c[(x <= 100) & (x >= 40)] = 10e-7 #kg/m^3 
# Typical seeding concentrations are usually less than 0.1 micrograms/liter, or 10e-7 kg/m^3

# Establishing wind velocity using a sine curve
# Typical wind speed in Colorado Springs is usually ~4.5 m/s

a = 100
b = 80
velocity = np.sin(x / a + b) + 5 #m/s
print(velocity) # checking to make sure wind velocity is in the range of typical Colorado Springs patterns

# Plot velocity to make sure it seems reasonable
fig0, ax0 = plt.subplots(1,1)
ax0.plot(x, velocity, label = 'Velocity', color = 'green')
ax0.set_xlabel('Distance (m)')
ax0.set_ylabel('Velocity (m/s)')
ax0.set_title ('Wind Velocity')
fig0.legend()
plt.show()

### SETTING UP MODEL PARAMETERS

# Establishing a timestep based on a stable courant number
# The courant number is stable at 1, so dt is solved for using a courant number of 1: dt = 1 * dt / u

dt = dx / np.max(velocity) # seconds - the maximum velocity value is most likely to cause instability, so the max velocity value is used to calculate dt for a stable courant number
courant = dt * velocity / dx # calculate courant number with stable dt
print(courant) # check that courant number is stable

### BOUNDARY CONDITIONS
# There will be zero concentration of seeding at the beginning and end.

### CONSTRUCT A MATRIX
# Because u is not constant, must use indexing

A = np.zeros((nodes, nodes))

for i in range(1, nodes):
    A[i, i] = 1 - courant[i] # center diagonal
    A[i, i-1] = courant[i] # left diagonal
A[0,0] = 1 # boundary condition that first node stays the same
print(A) # check the A matrix

### PLOT THE INITIAL CONDITIONS
fig1, ax1 = plt.subplots(1,1)
ax1.plot(x, c, label = 'Initial concentration', linestyle = '--', color = 'black')

### RUN THE MODEL THROUGH TIME
# This loop takes into the account additional silver iodide being pumped into the air every minute over the total 10 minutes

seconds = 0 #sec
endtime = 10 * 60 #s (600sec = 10mins)
while seconds <= endtime:
    newc = np.dot(A, c) # take the dot product of the A matrix and the concentrations
    c[:] = newc * 1 # substitute the results of the dot product into the concentration array
    if int(seconds) % 60 == 0: # concentration is added every 60 seconds
        if seconds > 0:
            ax1.plot(x, c, label = '%s minutes' % (int(seconds)/60)) # plotting the added concentration
            c[2:6] += 10e-7 # adding the concentration
    seconds += dt

### PLOTTING THE RESULTS
ax1.plot(x, c, label ='10 minutes')
ax1.set_xlabel('Distance (m)')
ax1.set_ylabel('Concentration (kg/m^3)')
ax1.set_title('Part 2: Transient Silver Iodide Concentration over 10 Mins', fontsize = 14)
fig1.legend()
plt.show()