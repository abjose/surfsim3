

def id_node(**kwargs):
    constraints = []
    for k,v in kwargs.items():
        def f(node, k=k, v=v): return eval('node.'+k) == v
        constraints.append(f)
    return constraints


def eval_id(node, constraints): # better name?
    return all([f(node) for f in constraints])
