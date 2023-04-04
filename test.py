# import torch
# input = torch.Tensor([[5, 0.5, 1, 0.5],[5, 0.5, 1, 0.5],[5, 0.5, 1, 0.5]])
# #有放回
# output = torch.multinomial(input, num_samples=100, replacement=True)
# print(output)

from utils import Ball
import matplotlib.pyplot as plt
import numpy as np
ball = Ball()
pos_init = (5,0,0)
vel_init = (0,0,-10)
print(pos_init,vel_init)
poses = [(pos_init[0],pos_init[2])]
for t in range(0,10):
    pos, vel = ball.observe(pos_init,vel_init,t*0.25)
    print(pos, vel)
    # if pos[2] >= 0:
    poses.append((pos[0],pos[2]))
poses = np.array(poses)
plt.scatter(poses[:,0],poses[:,1])
plt.gca().set_aspect(1)
plt.show()