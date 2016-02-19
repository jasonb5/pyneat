from . import Gene
from ml.ann import RecurrentNeuralNetwork as RNN

import copy
import math
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

    def crossover(self, dad, mom_fitness, dad_fitness, innovs):
        """Crossover between two genomes.

        To perform crossover the best performing genome is set to g1 and the
        other to g2. For matching genes there is a 50/50 chance to inherit
        from either parent. Disjoint genes are inheritted from the fitess
        parent by default. Finally the neuron structure is determined and
        the new baby is returned.

        Args:
            dad = Dad genome.
            mom_fitness = Mothers fitness.
            dad_fitness = Dad fitness.
            innovs = Instance of Innovations class

        Returns: New baby genome.
        """
        mom_genes = dict(map(lambda x: (x.innov, x), self.genes))
        dad_genes = dict(map(lambda x: (x.innov, x), dad.genes))

        if mom_fitness > dad_fitness:
            g1 = mom_genes
            g2 = dad_genes
        else:
            g1 = dad_genes
            g2 = mom_genes

        baby_genes = []

        for innov, gene in g1.items():
            if (innov in g2 and g2[innov].enabled and random.random() < 0.5):
                baby_genes.append(copy.deepcopy(g2[innov]))
            else:
                baby_genes.append(copy.deepcopy(g1[innov]))

        neurons = {}

        for g in baby_genes:
            if not g.inode in neurons:
                neurons[g.inode] = True
            
            if not g.onode in neurons:
                neurons[g.onode] = True

        inodes = filter(lambda x: x < self.neurons[0], neurons.keys())
        hnodes = filter(lambda x: (x >= self.neurons[0] and
            x < Genome.MAX_HIDDEN), neurons.keys())
        onodes = filter(lambda x: x >= Genome.MAX_HIDDEN, neurons.keys())

        baby = Genome(innovs.next_genome(), 
                [len(inodes), len(hnodes), len(onodes)],
                baby_genes)

        return baby

    def genesis(self):
        """Generates phenotype from genotype.

        Creates neural network describe by the genotype.
        """
        neurons = {}

        # Create dictionary using neuron ids for easy conversion from
        # relative indexes to absolute indexes, e.g. neurons ids 
        # (0, 1, 2, 3, 1000, 1001) map to (0, 1, 2, 3, 4, 5).
        for g in self.genes:
            if not g.inode in neurons:
                neurons[g.inode] = True

            if not g.onode in neurons:
                neurons[g.onode] = True

        sneurons = sorted(neurons.keys())
        
        net = RNN(self.neurons, lambda x: 1/(1+math.exp(-x)))

        for g in self.genes:
            inode = sneurons.index(g.inode)
            onode = sneurons.index(g.onode)

            net.add_link(inode, onode, random.random()*4.0-2.0)

        return net

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

    def mutate_weights(self):
        """Mutates all gene weights
        """
        for g in self.genes:
            g.weight = random.random()*4.0-2.0

    def mutate_gene(self, innovations):
        """Mutation by adding link.

        Mutates a genome by adding a link between two random neurons. The 
        process of adding a link:
        
        1. Select two random neurons
        2. Check if link already exists, exit if so.
        3. Check if innovation already exists.
            3.a If the innovation exists, recreate the gene from stored
                information.
            3.b If the innovation doesn't exist, create the new gene and 
                record the innovation.

        Args:
            innovations: Instance of Innovations class.
        """
        n1 = self.random_neuron()
        n2 = self.random_neuron(False)

        check = map(lambda x: x.inode == n1 and x.onode == n2, self.genes)

        if not any(check):
            innov = innovations.check_gene(n1, n2)

            if innov:
                gene = innovations.create_gene_from_innov(innov)
            else:
                gene = Gene(n1, n2, 
                        random.random()*4.0-2.0, innovations.next_innov())

                innovations.create_gene_innov(gene)

            self.genes.append(gene)

    def mutate_neuron(self, innovations):
        """Mutation by adding neuron.

        Mutates genome by adding replacing a gene with a neuron and two
        new genes. The process of adding a neuron:

        1. Select a random link.
        2. Check if links disabled, if so exit otherwise disable.
        3. Check if innovation already exists.
            3.a If the innovation exists, recreate the neuron and two genes 
                from stored information.
            3.b If the innovation doesn't exist, create the neuron and two
                genes then record the innovation.

        Args:
            innovations: Instance of Innocations class.
        """
        g = random.choice(self.genes)

        if not g.enabled:
            return

        g.enabled = False

        innov = innovations.check_neuron(
                g.inode, g.onode, g.innov)

        if innov:
            g1, g2 = innovations.create_neuron_from_innov(innov)
        else:
            neuron = sum(self.neurons[:2])

            g1 = Gene(g.inode, neuron, 1.0, innovations.next_innov())

            g2 = Gene(neuron, g.onode, g.weight, innovations.next_innov())

            innovations.create_neuron_innov(g, g1, g2, neuron)

        self.neurons[1] += 1
        self.genes.append(g1)
        self.genes.append(g2)

    def compatible(self, conf, genome):
        """Tests if two genomes are compatible.

        Compatibility is calculated from the weighted number of disjoint 
        genes, and the weighted total average of the weight differences.
        To be compatible this must all be less than some threshold.

        Args:
            conf: Conf instance.
            genome: Genome we're testing against
        """
        g1 = dict(map(lambda x: (x.innov, x), self.genes))
        g2 = dict(map(lambda x: (x.innov, x), genome.genes))

        g1_disjoint = filter(lambda x: not x in g2, g1)
        g2_disjoint = filter(lambda x: not x in g1, g2)

        total_disjoint = len(g1_disjoint)+len(g2_disjoint)

        matching = filter(lambda x: x in g1, g2)

        total_avg = 0.0

        for innov in matching:
            total_avg += g1[innov].weight-g2[innov].weight

        total_avg /= float(len(matching))

        compat = (total_disjoint*conf.coef_disjoint+
                total_avg*conf.coef_matching)

        return compat < conf.compat_threshold


