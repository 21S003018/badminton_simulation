import numpy as np
import random
import torch
import torch.nn as nn
import torch.nn.functional as F

class PolicyNet(nn.Module):
    def __init__(self, state_dim=2+2+3, hidden_dim=32, action_dim=9):
        super(PolicyNet, self).__init__()
        self.hidden_layer = nn.Linear(state_dim, hidden_dim)
        self.action_layer = nn.Linear(hidden_dim, action_dim) # output a probability distribution for each recommended action
        self.landing_layer = nn.Linear(action_dim,3)

    def forward(self, x):
        x = self.hidden_layer(x)
        action_out = self.action_layer(F.relu(x))
        landing_out = self.landing_layer(F.relu(action_out))
        return action_out, landing_out


class ValueNet(nn.Module):
    def __init__(self, state_dim, hidden_dim, action_dim):
        super(ValueNet, self).__init__()
        self.fc1 = nn.Linear(state_dim + action_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, 1)

    def forward(self, x, a):
        cat = torch.cat([x, a], dim=1)
        x = F.relu(self.fc1(cat))
        return self.fc2(x)


class Player():
    def __init__(self) -> None:
        self.policy_net = PolicyNet()
        self.value_net = ValueNet()
        # load data
        self.data = None
        pass

    def sample_action(self, state):
        action_out, landing = self.policy_net(state)
        action_distribution = F.softmax(action_out, dim=1)
        action = torch.multinomial(action_distribution,1)
        # todo: should we process the landing_out?
        return action, landing

    # def landing_predict(self, state, action):
    #     return

    def train_policy_net(self, data):
        # todo
        return
    
    def train_value_net(self, data):
        # todo
        return


class RandomPolicy():
    def __init__(self) -> None:
        self.touch_limit = 2
        pass
    def sample_action(self,position,):
        x,_,z = position
        if z > self.touch_limit:
            return None
        v_z = random.randint(15,24)
        if x >= 0:
            return [-np.sqrt(30**2-v_z**2),0,v_z]
        if x < 0:
            return [np.sqrt(30**2-v_z**2),0,v_z]


