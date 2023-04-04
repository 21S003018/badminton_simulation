import numpy as np


class Court():
    def __init__(self) -> None:
        self.length = 13.40  # (m)
        self.width = 5.18
        self.net_height = 1.55
        self.serve_line2net = 2
        pass


class Ball():
    def __init__(self) -> None:
        self.g = 9.8  # (m/s^-2)
        self.n = 2
        self.mass = 5.19*1e-3  # (kg)
        self.v_terminal = 6.86  # (m/s)
        self.b = (self.mass*self.g) / (self.v_terminal**self.n)
        self.current_position = None
        self.current_velocity = None
        pass

    def observe(self, init_position, init_velocity, t):
        velocity_x_init, velocity_y_init, velocity_z_init = init_velocity[
            0], init_velocity[1], init_velocity[2]
        # calculate current velocity for horizontal
        velocity_horizontal_init = np.sqrt(
            velocity_x_init**2 + velocity_y_init**2) + 1e-6
        velocity_horizontal_current = (velocity_horizontal_init*self.v_terminal**2)/(
            velocity_horizontal_init*self.g*t + self.v_terminal**2)
        velocity_x_current = velocity_horizontal_current * \
            velocity_x_init/velocity_horizontal_init
        velocity_y_current = velocity_horizontal_current * \
            velocity_y_init/velocity_horizontal_init
        # calculate current position for horizontal
        x, y, z = init_position[0], init_position[1], init_position[2]
        horizontal_position_delta = self.v_terminal**2 / self.g * np.log((velocity_horizontal_init*self.g*t+self.v_terminal**2)/(self.v_terminal**2))
        x_current = x + horizontal_position_delta*velocity_x_init/velocity_horizontal_init
        y_current = y + horizontal_position_delta*velocity_y_init/velocity_horizontal_init
        # calculate current velocity and position for vertical
        delta_t = self.v_terminal/self.g*np.arctan(velocity_z_init/self.v_terminal)
        if velocity_z_init >= 0 and t-delta_t<=0:
            velocity_z_current = (velocity_z_init - self.v_terminal*np.tan(self.g*t/self.v_terminal))/(1+velocity_z_init/self.v_terminal*np.tan(self.g*t/self.v_terminal))
            z_current = z + self.v_terminal**2/self.g*np.log(np.sin(self.g*t/self.v_terminal+np.arctan(self.v_terminal/velocity_z_init))/np.sin(np.arctan(self.v_terminal/velocity_z_init)))
        if velocity_z_init > 0 and t-delta_t>0:
            a = (self.v_terminal-0)/(self.v_terminal+0)
            k = 2*self.g/self.v_terminal
            velocity_z_current = -self.v_terminal + 2*self.v_terminal/(1+a*np.exp(k*(t-delta_t)))
            z_current = z + self.v_terminal**2/self.g*np.log(np.sin(self.g*delta_t/self.v_terminal+np.arctan(self.v_terminal/velocity_z_init))/np.sin(np.arctan(self.v_terminal/velocity_z_init))) + self.v_terminal*(t-delta_t) + 2*self.v_terminal/k*(np.log(1+a)-np.log(1+a*np.exp(k*(t-delta_t))))
        if velocity_z_init <= 0:
            # a = (self.v_terminal-velocity_z_init)/(self.v_terminal+velocity_z_init)
            k = 2*self.g/self.v_terminal
            velocity_z_current = -self.v_terminal + 2*self.v_terminal*(self.v_terminal+velocity_z_init)/(self.v_terminal+velocity_z_init+(self.v_terminal-velocity_z_init)*np.exp(k*t))
            z_current = z + self.v_terminal*t + 2*self.v_terminal/k*np.log(2*self.v_terminal/(self.v_terminal+velocity_z_init+(self.v_terminal-velocity_z_init)*np.exp(k*t)))
        # conclude
        self.current_velocity = [velocity_x_current, velocity_y_current, velocity_z_current]
        self.current_position = [x_current,y_current,z_current]
        return self.current_position, self.current_velocity


