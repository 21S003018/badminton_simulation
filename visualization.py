from numpy import *
import matplotlib.pyplot as plt
from matplotlib import animation
from utils import Ball
 
ball = Ball()
pos_init = (6,0,2)
vel_init = (-18,0,24)

fig,ax=plt.subplots()
point = plt.scatter(pos_init[0],pos_init[2])
point.remove()
def update(i):
    pos, vel = ball.observe(pos_init,vel_init,i*0.025)
    # plt.cla()
    plt.scatter(pos[0],pos[2])
    # point.set_data(pos[0],pos[2])
    return
def init():
    return

ani=animation.FuncAnimation(fig=fig,func=update,frames=100,init_func=init,interval=25,blit=False,repeat=False)
plt.gca().set_aspect(1)
plt.ylim((0,10))
plt.xlim((-7,7))
ani.save("test.gif")