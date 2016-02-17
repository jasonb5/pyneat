from .genotype import Gene

class Innovations(object):
    """Tracks innovations.

    Maintains list of gene and neuron mutations, preventing the recreation
    of innovations that have already occurred.
    """
    def __init__(self):
        self.neuron_innov = []
        self.gene_innov = []
        self.innov = 0
        self.neuron = 0
        self.genome = 0

    def next_genome(self):
        next_id = self.genome

        self.genome += 1

        return next_id

    def next_innov(self):
        self.innov += 1

        return self.innov

    def check_gene(self, inode, onode):
        """Check if gene mutation exists.

        Matching criteria is the inode and onode of the link.
        """
        check = map(lambda x: 
                (x['inode'] == inode and x['onode'] == onode), 
                self.gene_innov)

        if any(check):
            return self.gene_innov[check.index(True)]

        return None

    def check_neuron(self, inode, onode, old_innov):
        """Check if neuron mutation exists.

        Matching criteria is the inode, onode, and innovation of the 
        gene we're replacing.
        """
        check = map(lambda x:
                (x['inode'] == inode and x['onode'] == onode and 
                    x['old_innov'] == old_innov),
                self.neuron_innov)

        if any(check):
            return self.neuron_innov[check.index(True)]

        return None

    def create_gene_from_innov(self, innov):
        return Gene(
                innov['inode'], 
                innov['onode'], 
                innov['weight']. 
                innov['innov'])

    def create_neuron_from_innov(self, innov):
        g1 = Gene(
                innov['inode'],
                innov['neuron'],
                1.0,
                innov['innov1'])

        g2 = Gene(
                innov['neuron'],
                innov['onode'],
                innov['weight'],
                innov['innov2'])

        return g1, g2

    def create_gene_innov(self, gene):
        attr = {
                'inode': gene.inode,
                'onode': gene.onode,
                'weight': gene.weight,
                'innov': gene.innov 
                }

        self.gene_innov.append(attr)

    def create_neuron_innov(self, old_gene, g1, g2, neuron):
        attr = {
                'inode': old_gene.inode,
                'onode': old_gene.onode,
                'weight': old_gene.weight,
                'old_innov': old_gene.innov,
                'innov1': g1.innov,
                'innov2': g2.innov,
                'neuron': neuron
                }

        self.neuron_innov.append(attr)
