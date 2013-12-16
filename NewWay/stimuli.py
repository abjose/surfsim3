
# make sure can reset externally, and can tell if has been reset recently
# ....actually don't really need to reset stimulus? At least not as important as for positioning. But might be nice.
# need to be able to pass position, get back stimulus

class Stimulus(object):
    def __init__(self, side, ...):
        self.steps = 0
        self.side  = side
        # don't worry about keeping track of how recently been reset for now
        self.output = None

    def reset(self):
        raise NotImplementedError("Need to define reset.")

    def step(self):
        raise NotImplementedError("Need to define step.")

    def get_dims(self):
        return (self.side, self.side)

    def stim_at_pos(self, (x,y)):
        return self.output[x,y] # not really needed



# TODO: Change name to GratingStim?
class SinusoidStim(Stimulus):
    def __init__(self, side, spacing=0.1, f=5, amp=1, step_size=.1):
        # On a sidexside size grid with each step spacing apart, insert
        # sin with freq f and amplitude amp. On step, increment by step_size.
        # TODO: add ability to change angle
        super(SinusoidStim, self).__init__(side)
        self.range  = np.arange(0,self.side*spacing, spacing)
        self.func   = lambda x: amp*np.sin(f*x + step_size*self.steps)
        self.step()

    def step(self):
        sin = self.func(self.range)
        self.output = np.resize(sin, (self.side, self.side))
        self.steps += 1


class JigglySinusoidStim(SinusoidStim):
    def __init__(self, side, max_jiggle):
        # every time step move up to (max_jiggle) steps in a random direction
        self.max_jiggle = max_jiggle
        super(JigglySinusoidStim, self).__init__(side)

    def step(self):
        sin = self.func(self.range)
        self.output = np.resize(sin, (self.side, self.side))
        self.steps += self.max_jiggle * (np.random.rand()*2. - 1.)


class InvertingSinusoidStim(SinusoidStim):
    def __init__(self, side, invert_steps):
        # will invert every invert_steps steps
        self.invert_steps = invert_steps
        self.sign = 1
        super(InvertingSinusoidStim, self).__init__(side)
        
    def step(self):
        sin = self.func(self.range)
        if self.steps % self.invert_steps == 0:
            self.sign *= -1
        self.output = np.resize(self.sign*sin, (self.side, self.side))
        self.steps += 1


class SquareWaveStim(Stimulus):
    def __init__(self, side, dt):
        super(SquareWaveStim, self).__init__(side)
        self.dt       = dt # half period in integer time ticks
        self.curr_vec = [-1.]*side
        # fill array initially
        for i in range(side):
            self.step()

    def step(self):
        self.curr_vec = self.curr_vec[1:] + [self.get_square(self.steps)]
        self.output = np.resize(self.curr_vec, (self.side, self.side))
        self.steps += 1

    def get_square(self, t, t0=0):
        return 0. if ((t-t0)%(2*self.dt)) < self.dt else 1.


class BarStim(Stimulus):
    def __init__(self, side, bar):
        super(BarStim, self).__init__(side)
        self.bar    = bar
        self.output = np.array([1.]*bar + [-1.]*(side-bar)) # (0,1) vs (-1,1)?
        self.output = np.resize(self.output, (self.side, self.side))
            
    def step(self):
        self.output = np.roll(self.output, 1, 1)


class FullFieldStim(Stimulus):
    def __init__(self, side, f):
        super(FullFieldStim, self).__init__(side)
        self.freq   = f
        self.output = np.array([1.]*side)
        self.output = np.resize(self.output, (self.side, self.side))
            
    def step(self):
        if self.steps % self.freq == 0:
            self.output = -1*self.output
        self.steps += 1


if __name__=='__main__':
    pass
