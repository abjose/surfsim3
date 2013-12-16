
import matplotlib.pyplot as plt
import networkx as nx

from node import Node


"""
Do most node manipulation here
"""


class Context(object):
    
    def __init__(self):
        # connection and hierarchy graphs
        self.hg = nx.Digraph()
        self.cg = nx.Digraph()
        # root node and focus
        self.root  = Node('root', self, ...)
        self.focus = self.root
        # keep them batches in line
        self.init_batches = ['pre_init', 'post_init']
        self.step_batches = ['interact', 'update']
        self.all_batches  = self.init_batches + self.run_batches





    def add_node(self, name, focus=False, **kwargs):
        """ Add node to current focus. Auto-change focus if 'focus' true. """
        n = Node(name, self, **kwargs)
        self.hg.add_edge(self.focus, n)
        if focus:
            self.focus = n

    def add_step(self, dest, step):
        self.focus.add_step(dest, step)

    def copy_node(self, ...):
        pass


    def filter_nodes(self, constraints, subset=None):
        # constraints should be list of boolean functions that take node
        # returns a set
        nodes = set()
        subset = subset if subset != None else self.hg.nodes()
        for node in subset:
            if all(map(lambda x: x(node), constraints)):
                nodes.add(node)                

    def set_focus(self, ...):
        # just pass constraints like before? ...
        pass

    def connect_nodes(self, source, target, weight):
        self.cg.add_edge(source, target, weight=weight)

    def init_simulation(self, ...):
        for batch in self.init_batches:
            for node in self.cg.nodes():
                node.run_batch(batch)

    def step_simulation(self, ...):
        for batch in self.step_batches:
            for node in self.cg.nodes():
                node.run_batch(batch)


   def show_hg(self):
        nx.draw(self.hg)
        plt.show()
    def show_cg(self):
        nx.draw(self.cg)
        plt.show()
