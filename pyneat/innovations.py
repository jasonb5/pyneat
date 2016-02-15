from .genotype import Gene

class Innovations(object):
    def __init__(self):
        self.neuron_innov = []
        self.gene_innov = []
        self.innov = 0
        self.neuron = 0

    def next_innov(self):
        self.innov += 1

        return self.innov

    def check_gene(self, inode, onode):
        check = map(lambda x: 
                (x[1] == inode and x[2] == onode), self.gene_innov)

        if any(check):
            return self.gene_innov[check.index(True)]['innov']

        return None

    def create_gene_from_innov(self, innov_id):
        innov = filter(lambda x: x[0] == innov_id, self.gene_innov)[0]

        return Gene.from_attributes(innov)

    def create_gene_innov(self, gene):
        self.gene_innov.append(gene.get_attributes())
