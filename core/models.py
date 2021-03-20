from dto import Data


class LpSolve(object):
    def __init__(self, data: Data):
        self.c = None
        self.x = None
        self.vars = None
        self.problem = None

    def run(self):
        self.problem.solve()

    def get_result(self) -> dict:
        pass
