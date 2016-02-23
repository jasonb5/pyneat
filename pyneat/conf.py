class Conf(object):
    def __init__(self):
        self.pop_size = 150
        self.coef_matching = 0.4
        self.coef_disjoint = 2.0
        self.compat_threshold = 1.0
        self.survival_rate = 0.2
        self.stagnation_threshold = 15
        self.mate_only_prob = 0.2
        self.mutate_only_prob = 0.25
        self.mutate_neuron_prob = 0.03
        self.mutate_gene_prob = 0.05
        self.mutate_power = 2.5
