
# make sure can reset externally
# and can tell if has been reset recently?


class Positioner(object):
    # this might not be the best format to settle on
    # can't really guarantee any order
    def __init__(self):
        self.positions = []

    #def get_position(self, n):
    #    # get nth position?
    #    pass
    
    def get_next(self):
        if len(self.positions) > 0:
            return self.positions.pop()
        else:
            raise Exception('Trying to get too many position points.')

    def reset(self):
        raise NotImplementedError("Need to define reset.")


class Line(Positioner):
    def __init__(self):
        super(Line, self).__init__()

class Grid(Positioner):
    def __init__(self, x0=0, y0=0, dx=1, dy=1, xl=10, yl=10):
        super(Grid, self).__init__()
        # just store an array of positions...
        xs = range(x0, xl, dx)
        ys = range(y0, yl, dy)
        self.reset()

    def reset(self):
        self.positions = [(x,y) for x in xs for y in ys]
