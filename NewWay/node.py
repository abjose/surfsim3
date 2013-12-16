
import network as nx


"""
NODE IS SIMPLE MAN
NODE NOT NEED KNOW ABOUT OTHER NODES IN BIG FANCY SIMULATION
NODE JUST KEEP TO SELF AND DO WHAT BIG CONTEXT TELL HIM


TODO: Make a function called make_connect_function or something that allows you
      to pass various parameters and it will return the desired function.
TODO: When connecting after initialization, should add connection function to
      list? 
TODO: Should make some functions for easily creating constraints based on name,
      distance, etc.
TODO: define more nodes (like time node, etc.) that basically just auto-add some
      stuff to batches?
"""


class Node(object):
    
    def __init__(self, name, context,
                 position=None, 
                 IRF=None, data_len=None, output_len=50, output_offset=0,
                 is_worker=False, inherit_position=True):
        # TODO: actually make use of all those kwargs
        # TODO: Maybe add some more useful default values?
        # context reference
        self.C = context
        # batch container
        self.batches = dict([(r, []) for r in self.C.all_batches])
        # hold input set
        self.input_list = []
        # IRF, data and output stuff
        self.IRF  = IRF
        self.data = []
        self.data_len = data_len
        # make long enough to convolve nicely if nothing provided
        if data_len == None:
            self.data_len = output_len + len(IRF) - 1
        # ticks back from most recent to have as output - 0 is most recent
        self.output_offset = output_offset 
        self.output_len   = output_len
        # weighting function
        # don't have this, what if want different weighting functions?
        #self.weight_func = ??
        # position
        self.pos = position
        # also have positioning function for sub-nodes? ehh
        # for holding new output before update
        self.temp_data = []
        # automatically add some steps if desired
        if is_worker:
            # initialize vectors
            self.add_step('pre_init', store(self.init_data))
            # harvest inputs and multiply by weights
            self.add_step('interact', store(self.get_inputs))
            # move temp_data to data
            self.add_step('update', store(self.update_data))


    def add_step(self, dest, step):
        self.batches[dest].append(step)

    def run_batch(self, batch_name, ):
        for step in self.batches[batch_name]:
            self.run(step)

    def init_data(self):
        self.data = nx.array([0.]*data_len)
        self.temp_data = nx.array([0.]*data_len)


    def get_parent(self):
        parent = self.C.hg.predecessors(self)
        if len(parent) > 1: raise Exception('Multiple parents?!')
        return parent[0]

    def get_pos(self):
        # could alternately redefine get_attr and check to see if it's pos
        # (and maybe ignore anything else)
        if self.pos == None and self.inherit_position:
            return self.get_parent().get_pos()
        else:
            return self.pose

    def output(self):
        start, end = self.output_start, self.output_start + self.output_len
        return self.data[start:end]

    def dot_vector(self, vec):
        assert len(vec) >= len(self.irf)
        # need to reverse irf to convolve
        return np.dot(vec[-len(self.IRF):], self.IRF[::-1])

    def sum_vectors(self, vec_list):
        return np.sum(vec_list, 0)

    def update_data(self):
        # just move from temp_data to data
        self.data = self.temp_data.copy() # copy necessary?

    # need 'clean_data'?

    def get_inputs(self):
        # should get inputs and multiply by weights, and put into input_list
        self.input_list = []
        for source in self.C.cg.predecessors(self):
            weight = self.C.cg[source][self]['weight']
            self.input_list.append(weight * source.output())

    def connect_to(self, constraints, weight_func):
        # NOTE: could have more specific contraints, like 'name=...' rather than
        # generic list...
        # constraints: list of boolean functions that take nodes
        # weight_func: function that takes source, target nodes, returns weight 
        targets = self.C.filter_nodes(constraints)
        for target in targets:
            self.C.connect_nodes(self, target, weight_func(self, target))

    def connect_from(self, constraints, weight_func):
        # constraints should be list of boolean functions that take nodes
        # weight_func: function that takes source, target nodes, returns weight 
        sources = self.C.filter_nodes(constraints)
        for source in sources:
            self.C.connect_nodes(source, self, weight_func(source, self))

    def store(self, f, *args, **kwargs):
        """ Take a function, args, and kwargs; return tuple for storage. """
        return f, args, kwargs

    def run(self, stored):
        f, args, kwargs = stored
        f(*args, **kwargs)


 
class InputNode(Node):

# should be able to reset input_func and pos_func when sim is reset?
# how not do reset multiple times?
# could just track whether has been reset recently from stimulus/positioning
    
    def __init__(self, input_func, pos_func, ..., **kwargs):
        super(InputNode, self).__init__()

#class SumNode
#class IRFNode
#class DelayNode
#class SumAndIRFNode
