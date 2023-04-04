import gym
from gym import spaces
from utils import *
from policy import RandomPolicy
from const import *
import pickle as pkl

class RandGame(gym.Env):
    def __init__(self):
        self.court = Court()
        self.ball = Ball()
        self.ball_track = []
        self.unit_time = 0.025

        self.action_space = spaces.Box(low=np.array([-np.inf,-np.inf,-np.inf]),high=np.array([np.inf,np.inf,np.inf]),shape=(3,))
        self.observation_space = spaces.Dict(spaces={
            POS: spaces.Box(low=np.array([-6.7,0,0]),high=np.array([6.7,5.18,np.inf]),shape=(3,)),
            VEL: spaces.Box(low=np.array([-np.inf,-np.inf,-np.inf]),high=np.array([np.inf,np.inf,np.inf]),shape=(3,))
        })

        # self.init_state = self.observation_space.sample()
        self.init_state = {
            POS:[6,self.court.width/2,1.15],
            VEL:[0,0,0],
        }
        self.current_state = self.init_state
        return

    def step(self, action:np.array):
        # update state
        if action == [0,0,0]:
            next_pos, next_vel = self.ball.observe(self.current_state[POS], self.current_state[VEL], self.unit_time)
            if not self.cross_net(next_pos) or self.out(next_pos):
                reward = None # todo
                done = True
                if not self.cross_net(next_pos):
                    info = {"fail to cross net"}
                if self.out(next_pos):
                    info = {"out"}
                self.current_state = {
                    POS:next_pos,
                    VEL:next_vel,
                }
            else:
                reward = None # todo
                done = False
                info = {"normal update"}
                self.current_state = {
                    POS: next_pos,
                    VEL: next_vel,
                }
            return self.current_state, reward, done, info
        reward = None # todo
        done = False
        info = {"stroke"}
        self.current_state[VEL] = action
        return self.current_state, reward, done, info


    def cross_net(self,next_pos):
        # judge if the ball could cross net in the next unit time
        current_x,current_y,current_z = self.current_state[POS]
        next_x,next_y,next_z = next_pos[0], next_pos[1], next_pos[2]
        if current_x * next_x >= 0:
            return True
        if current_z-current_x*(next_z-current_z)/(next_x-current_x) < self.court.net_height:
            return False
        else:
            return True

    def out(self,pos):
        # judge if the current position is out of the court
        height_threshold = 1 # if the height is lower than this threshold, we think ...
        x,y,z = pos[0], pos[1], pos[2]
        return not ((x <= self.court.length/2 and x >= -self.court.length/2) and (y >= 0 and y <= self.court.width))

    def run(self,note=""):
        p1 = RandomPolicy() # serve
        p2 = RandomPolicy()
        stroker = p1
        print("position:",self.current_state[POS], "velocity:", self.current_state[VEL])
        self.ball_track.append(self.current_state[POS].copy())
        while True:
            pos = self.current_state[POS]
            x,y,z = pos
            vel = self.current_state[VEL]
            v_x,v_y,v_z = vel
            if v_x * x < 0 or z > 2:
                state, reward, done, info = self.step([0,0,0])
                print("position:",self.current_state[POS], "velocity:", self.current_state[VEL])
                self.ball_track.append(self.current_state[POS].copy())
            else:
                action = stroker.sample_action(pos)
                if stroker == p1:
                    print("p1 stroke:", action)
                    stroker = p2
                else:
                    print("p2 stroke:", action)
                    stroker = p1
                state, reward, done, info = self.step(action)
                print("position:",self.current_state[POS], "velocity:", self.current_state[VEL])
            if done:
                print(info)
                break               
        return

    def reset(self):
        self.current_state = self.init_state
        pass

    def render(self):
        pass

    def save_ball_track(self,path="data/ball_track.pkl"):
        with open(path, "wb") as f:
            pkl.dump(self.ball_track, f)
        return