import json

class Conf(object):
    def __init__(self, **kwargs):
        self.generations = kwargs.get('generations', 100)
        self.pop_size = kwargs.get('pop_size', 150)
        self.coef_matching = kwargs.get('coef_matching', 0.4)
        self.coef_disjoint = kwargs.get('coef_disjoint', 1.0)
        self.compat_threshold = kwargs.get('compat_threshold', 3.0)
        self.survival_rate = kwargs.get('survival_rate', 0.2)
        self.stagnation_threshold = kwargs.get('stagnation_threshold', 15)
        self.mate_only_prob = kwargs.get('mate_only_prob', 0.2)
        self.mutate_only_prob = kwargs.get('mutate_only_prob', 0.25)
        self.mutate_neuron_prob = kwargs.get('mutate_neuron_prob', 0.03)
        self.mutate_gene_prob = kwargs.get('mutate_gene_prob', 0.05)
        self.mutate_power = kwargs.get('mutate_power', 2.5)
        self.fitness_func = kwargs.get('fitness_func', "")
        self.num_input = kwargs.get('num_input', 3)
        self.num_output = kwargs.get('num_output', 1)
        self.runs = kwargs.get('runs', 1)
        self.allow_recurrent = kwargs.get('allow_recurrent', False)

    def to_json(self):
        return json.dumps(self.__dict__)
