import json

class Conf(object):
    def __init__(self):
        self.generations = 100
        self.pop_size = 150
        self.coef_matching = 0.4
        self.coef_disjoint = 1.0
        self.compat_threshold = 3.0
        self.survival_rate = 0.2
        self.stagnation_threshold = 15
        self.mate_only_prob = 0.2
        self.mutate_only_prob = 0.25
        self.mutate_neuron_prob = 0.03
        self.mutate_gene_prob = 0.05
        self.mutate_power = 2.5
        self.fitness_func = None
        self.num_input = 3
        self.num_output = 1
        self.runs = 1

    def to_json(self):
        return json.dumps(self.__dict__)
