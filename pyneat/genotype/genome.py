from . import Gene

class Genome(object):
    """Genotype of an ANN.

    Represents the genotype of an ANN. Provides methods to mutate a genome
    through adding nodes and links, enabling/disabling links, and changing 
    the weights of links in the network. The genotype is used to produce
    the phenotype of a network.

    Attributes:
        neurons: 3-tuple input, hidden, and output neurons 
        genes: list of genes describing the links between neurons
    """

    MAX_HIDDEN = 1000

    def __init__(self, neurons, genes):
        self.neurons = neurons
        self.genes = genes

    @classmethod
    def minimal_fully_connected(cls, neurons):
        """Creates fully connected network.

        Creates fully connected network only containing the input and output
        neurons.

        Args:
            neurons: 2-tuple input, and output neurons
        """
        innov = 0
        genes = []

        for i in xrange(neurons[0]):
            for o in xrange(neurons[1]):
                genes.append(Gene(i, Genome.MAX_HIDDEN+o, 1.0, innov))

                innov += 1

        return cls((neurons[0], 0, neurons[1]), genes)
