######################################################################
# This file copyright the Georgia Institute of Technology
#
# Permission is given to students to use or modify this file (only)
# to work on their assignments.
#
# You may NOT publish this file or make it available to others not in
# the course.
#
######################################################################

#These import statements give you access to library functions which you may
# (or may not?) want to use.
from math import *
from glider import *
import copy



#This is the function you will have to write for part A. 
#-The argument 'height' is a floating point number representing 
# the number of meters your glider is above the average surface based upon 
# atmospheric pressure. (You can think of this as hight above 'sea level'
# except that Mars does not have seas.) Note that this sensor may be off
# a static  amount that will not change over the course of your flight.
# This number will go down over time as your glider slowly descends.
#
#-The argument 'radar' is a floating point number representing the
# number of meters your glider is above the specific point directly below
# your glider based off of a downward facing radar distance sensor. Note that
# this sensor has random Gaussian noise which is different for each read.

#-The argument 'mapFunc' is a function that takes two parameters (x,y)
# and returns the elevation above "sea level" for that location on the map
# of the area your glider is flying above.  Note that although this function
# accepts floating point numbers, the resolution of your map is 1 meter, so
# that passing in integer locations is reasonable.
#
#
#-The argument OTHER is initially None, but if you return an OTHER from
# this function call, it will be passed back to you the next time it is
# called, so that you can use it to keep track of important information
# over time.
#
def measurement_prob(predicted_height,measured_height):
    prob = 1.0
    mu = measured_height
    prob *= Gaussian(mu,25,predicted_height)
    return prob

def Gaussian(mu,sigma,x):
    return exp(-((mu-x)**2)/(sigma**2)/2.0)/sqrt(2.0*pi*(sigma**2))

def estimate_next_pos(height, radar, mapFunc, OTHER=None):

    """Estimate the next (x,y) position of the glider."""

   #example of how to find the actual elevation of a point of ground from the map:
   #actualElevation = mapFunc(5,4)
    N = 30000
    N_new = 1000
    global x_sum 
    global y_sum 
    global xy_estimate 
    global p
    global p3
    if OTHER == None:
        OTHER = []
        p=[]
        for i in range(N):
             x = (random.random()*500)-250
             y = (random.random()*500)-250
             heading = random.gauss(0,pi/4)
             z = height
             r = glider(x=x,y=y,z=z,heading=heading,mapFunc=mapFunc)
             r.set_noise(new_m_noise=0.7)
             p.append(r)
        H=[]
        for i in range(N):
            H.append(p[i].sense())
        w=[]
        weight_sum = 0
        for i in range(N):
            weight = measurement_prob(height-radar,mapFunc(p[i].x,p[i].y))
            weight_sum += weight
            w.append(weight)
        p3=[]
        index = int(random.random()*N)
        beta = 0.0
        mw = max(w)
        #N_new = 1000
        #delta = 1.0/N_new
        #j=0
        #sp=w[j]
        #for i in range(N_new):
         #   r = (random.random()+i)*delta
          #  while sp<r:
           #     j += 1
           #     sp +=w[j]
            #p3.append(copy.deepcopy(p[index]))

        for i in range(N_new):
          beta += random.random()*2.0*mw
          while beta>w[index]:
               beta -= w[index]
               index = (index+1)%N
          p3.append(copy.deepcopy(p[index]))

        for i in range(N_new):
            p3[i].glide()
            OTHER.append(p3[i])
        x_sum =0
        y_sum =0
        for i in range(N_new):
            x_sum += p3[i].x 
            y_sum += p3[i].y 
        xy_estimate = (x_sum/N_new,y_sum/N_new)
        OTHER = p3
        #print(x_sum/N_new,y_sum/N_new)
    if OTHER != None:
        N = len(OTHER)
        p=[]
        for i in range(N):
            p.append(OTHER[i])
        
        H=[]
        for i in range(N):
            H.append(p[i].sense())
        w=[]
        for i in range(N):
            weight = measurement_prob(height-radar,mapFunc(p[i].x,p[i].y))
            w.append(weight)
        p3=[]
        index = int(random.random()*N)
        beta = 0.0
        mw = max(w)
        N_new = 1000
        for i in range(N_new):
            beta += random.random()*2.0*mw
            while beta>w[index]:
                beta -= w[index]
                index = (index+1)%N
            p3.append(copy.deepcopy(p[index]))
        for i in range(int(0.15*N_new)):
            index = int(random.random()*N_new)
            x = p3[index].x
            y = p3[index].y
            heading = p3[index].heading
            x = x+random.uniform(-3,3)
            y = y+random.uniform(-3,3)
            heading = heading + random.uniform(-pi/8,pi/8)
            newp=glider(x=x,y=y,heading=heading,mapFunc=mapFunc)
            p3[index]=newp
        for i in range(N_new):
            p3[i].glide()
            OTHER.append(p3[i])
        x_sum =0
        y_sum =0
        for i in range(N_new):
            x_sum += p3[i].x 
            y_sum += p3[i].y
        xy_estimate = (x_sum/N_new,y_sum/N_new)
        OTHER = p3
  
     # You must return a tuple of (x,y) estimate, and OTHER (even if it is NONE)
     # in this order for grading purposes.
     #
     #xy_estimate = (0,0)  #Sample answer, (X,Y) as a tuple.
  
     #TODO - remove this canned answer which makes this template code
     #pass one test case once you start to write your solution.... 
     #xy_estimate = (391.4400701739478, 1449.5287170970244) 
  
     # You may optionally also return a list of (x,y,h) points that you would like
     # the PLOT_PARTICLES=True visualizer to plot for visualization purposes.
     # If you include an optional third value, it will be plotted as the heading
     # of your particle.
  
    optionalPointsToPlot = [ (1,1), (2,2), (3,3) ]  #Sample (x,y) to plot 
    optionalPointsToPlot = [ (1,1,0.5),   (2,2, 1.8), (3,3, 3.2) ] #(x,y,heading)
  
  
    return xy_estimate, OTHER, optionalPointsToPlot
  
  
  # This is the function you will have to write for part B. The goal in part B
  # is to navigate your glider towards (0,0) on the map steering # the glider 
  # using its rudder. Note that the Z height is unimportant.
  
  #
  # The input parameters are exactly the same as for part A.
def desired_angle(x,y):

    return atan2(y,x)


def next_angle(height, radar, mapFunc, OTHER=None):
  
     #How far to turn this timestep, limited to +/-  pi/8, zero means no turn.
    steering_angle = 0.0
    
    if OTHER == None:
            OTHER = {}
            xy,O,op = estimate_next_pos(height=height,radar=radar,mapFunc=mapFunc,OTHER=None)
            OTHER_estimate = O
            OTHER_next     = 0
            OTHER={1: OTHER_estimate,2: OTHER_next,3:0,4:0}   
            #print(len(OTHER_estimate))

    else:
       # print(len(OTHER[1]))
        OTHER_estimate =[]
        #for i in OTHER[1]:
        #print(type(OTHER[1]))
        OTHER_estimate=OTHER[1]
        OTHER_next     = OTHER[2]
        if OTHER_next <= 50:
            xy,O,op = estimate_next_pos(height,radar,mapFunc,OTHER=list(OTHER_estimate))
            #print(len(O))
            OTHER_estimate = O
            OTHER_next += 1
            x_est = xy[0]
            y_est = xy[1]
        else:
            
            xy,O,op = estimate_next_pos(height,radar,mapFunc,OTHER=list(OTHER_estimate))
            da=angle_trunc(desired_angle(xy[0],xy[1]))
            p=[]
            p=O
            ca = 0
            #for i in range(len(p)):
            #    ca += p[i].heading
            #ca = ca/len(p)
            #curr_x = 0
            #curr_y = 0
            #for i in range(len(p)):
            #    curr_x += p[i].x
            #    curr_y += p[i].y
            #curr_x = curr_x/len(p)
            #curr_y = curr_y/len(p)
            ca = desired_angle(OTHER[3]-xy[0],OTHER[4]-xy[1])
            ca = angle_trunc(ca)
            ra=angle_trunc(da-ca)
            steering_angle = min(pi/8,max(ra,-pi/8))
            steering_angle = angle_trunc(steering_angle)
            for i in range(len(p)):
                p[i].heading += steering_angle
                p[i].glide(rudder=steering_angle)
            x_est = 0
            y_est = 0
            for i in range(len(p)):
                x_est += p[i].x
                y_est += p[i].y
            x_est = x_est/len(p)
            y_est = y_est/len(p)
            OTHER_estimate = p
            OTHER_next += 1
        OTHER = {}
        OTHER={1:OTHER_estimate,2:OTHER_next,3:x_est,4:y_est}

 
     # You may optionally also return a list of (x,y)  or (x,y,h) points that 
     # you would like the PLOT_PARTICLES=True visualizer to plot.
     #
     #optionalPointsToPlot = [ (1,1), (20,20), (150,150) ]  # Sample plot points 
     #return steering_angle, OTHER, optionalPointsToPlot
    return steering_angle, OTHER
