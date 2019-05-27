import json
import numpy as np
import matplotlib.pyplot as plt
import random as rnd
import os
import time

dirname = os.getcwd()+time.strftime("%d_%m_%Y_%T")
os.mkdir(str(dirname)+"_data")
os.mkdir(str(dirname)+"_images")
    
for imgstr in range(500):
    #Making the image frame
    nt = 20 #length and width of frame
    nth = (nt-2.0)/2.0
    dum = np.ones((nt,nt)) #dum is the np.array containing all pixels
    
    
    classes = ['ne','nw','sw','se'] #set of possible directions
    classes_b = [[1,1],[1,-1],[-1,-1],[-1, 1]] #corresponding values
    diri = np.random.randint(4) #random choice
    b = classes_b[diri] #b determines direction to 2nd boot
    label = classes[diri]
    
    pts = np.random.randint(2,high=(nt-2),size=(1,2)) #First boot
    
    a = min(pts[0,0],abs(nt-pts[0,0]),pts[0,1],abs(nt-pts[0,1])) #position limits
    #       maximum size. Note: this could be improved. By taking into account b, 
    #       larger triangles could be placed into the edge.
    c = np.random.randint(min(a,1),high=max(a,2),size=(1,2)) # distance to 2nd boot
    pts = np.concatenate((pts,np.abs(pts+b*c))) #adds second boot to pts array
    
    pts3 = np.array([[pts[0,0],pts[1,1]]]) # third point completes the vertices
    pts = np.concatenate((pts,pts3))
    ptsl = pts.tolist()
    #Filling in the boots with zeros
    dum[pts[0,0],pts[:,1].min():pts[:,1].max()+1]=0 
    dum[pts[:,0].min():pts[:,0].max()+1,pts[1,1]]=0
    
    #For Matplotlib plotting
    for i in range(int(np.abs(pts[1]-pts[2]).max())):
        ptsl.append([pts[1,0]-i*np.sign((pts[1]-pts[2]).mean()),pts[1,1]])
    for i in range(int(np.abs(pts[0]-pts[2]).max())):
        ptsl.append([pts[0,0],pts[0,1]-i*np.sign((pts[0]-pts[2]).mean())])
    ####    To determine visually which corner is which:
    #for i in range(3):
    #    d=i+4
    #    dum[pts[i,0],pts[i,1]]=0
    ####
    #Important parameters
    m = (pts[0,1]-pts[1,1])/(pts[0,0]-pts[1,0]) #slope of hypotenuse 
    dy = pts[0,0]-pts[1,0] #Confusing: x coordinate specified by y position
    dx = pts[0,1]-pts[1,1]
    ady = np.abs(dy) #specifies distance to fill-in
    adx = np.abs(dx) #specifies distance to fill-in
    #Filling in the rest of the triangle
    for yy in range(ady-1): 
        y = pts[2,0]-np.sign(dy)*(yy+1)
        for xx in range(adx-(int(np.round((yy+1)*abs(m))))): #Jump accords to slope
            x = pts[2,1]+np.sign(dx)*(xx+1)
            dum[y,x]=0
            ptsl.append([y,x]) #for matplotlib plotting
    #Data and label in one variable.
    #s = [dum,label]
    
    #Write data to file
    ptsl=np.array(ptsl)
    os.chdir(str(dirname)+"_data")
    f = open('ptl'+str(imgstr)+'_'+str(label)+'.txt','w')
    json.dump(dum.tolist(),f)
    f.close()
    
    #plot figure
    fig = plt.figure()
    plt.scatter(ptsl[:,1],nt-ptsl[:,0])
    plt.xlim((0,nt))
    plt.ylim((0,nt))
    plt.axis('off')

    #Save figure
    os.chdir("..")
    os.chdir(str(dirname)+"_images")
    fig.savefig('ptl'+str(imgstr)+'_'+str(label)+'.png')
    plt.close()
