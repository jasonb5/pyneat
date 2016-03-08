class Organism(object):
    def __init__(self, genome):
        self.genome = genome
        self.fitness = 0.0
        self.rank = 0
        self.marked = False
        self.winner = False

    def marked_death(self):
        self.marked = True
