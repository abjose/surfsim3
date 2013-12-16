


class IRF(object):
    
    def __init__(self):
        pass

    def make_test_irf(self, a, b):
        
        def test_irf(c, d):
            return a + b + c + d

        return test_irf
