from pyneat import Innovations
from pyneat.genotype import Genome

import mock
import random

def test_genome():
    genome = Genome.minimal_fully_connected(0, (3, 2))

    assert genome.neurons == [3, 0, 2]
    assert len(genome.genes) == 6

def test_mutate_gene():
    genome = Genome.minimal_fully_connected(0, (3, 2))

    genome.neurons[1] += 1

    innovations = Innovations()

    innovations.innov = max(map(lambda x: x.innov, genome.genes))

    print innovations.innov

    random.choice = mock.MagicMock(side_effect=[0, 3])

    genome.mutate_gene(innovations)

    assert len(genome.genes) == 7
    assert len(innovations.gene_innov) == 1
