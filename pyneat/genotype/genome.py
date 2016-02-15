from . import Gene

import copy
import random

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

    def __init__(self, genome_id, neurons, genes):
        self.genome_id = genome_id
        self.neurons = neurons
        self.genes = genes

    @classmethod
    def minimal_fully_connected(cls, genome_id, neurons):
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

        return cls(genome_id, [neurons[0], 0, neurons[1]], genes)

    def duplicate(self, genome_id):
        """Duplicates genome.

        Args:
            genome_id: new genomes id.

        Returns:
            Deep copy of current genome, with a new id.
        """
        genome = copy.deepcopy(self)

        genome.genome_id = genome_id

        return genome

    def random_neuron(self, allow_input=True):
        """Chooses random neuron.

        Builds a list of possible neurons and selects a random one.

        Args:
            allow_input: Whether to consider input neurons.

        Returns:
            Random neuron.
        """
        pool = {}

        if allow_input:
            for x in xrange(self.neurons[0]):
                pool[x] = True

        for x in xrange(self.neurons[1]):
            pool[x] = True

        for x in xrange(self.neurons[2]):
            pool[Genome.MAX_HIDDEN+x] = True

        return random.choice(pool.keys())

    def mutate_gene(self, innovations):
        """Mutation by adding link.

        Mutates a genome by adding a link between two random neurons. The 
        process of adding a link:
        
        1. Check if link already exists, exit if so.
        2. Check if innovation already exists.
            2.a If the innovation exists, recreate the gene from stored
                information.
            2.b If the innovation doesn't exist, create the new gene and 
                record the innovation.

        Args:
            innovations: Instance of Innovations class.
        """
        n1 = self.random_neuron()
        n2 = self.random_neuron(False)

        check = map(lambda x: x.inode == n1 and x.onode == n2, self.genes)

        if not any(check):
            innov_id = innovations.check_gene(n1, n2)

            if innov_id:
                gene = innovations.create_gene_from_innov(innov_id)
            else:
                gene = Gene(n1, n2, 
                        random.random()*4.0-2.0, innovations.next_innov())

                innovations.create_gene_innov(gene)

            self.genes.append(gene)
