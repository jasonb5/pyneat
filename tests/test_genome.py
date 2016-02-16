from pyneat import Conf
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

    old = random.choice

    random.choice = mock.MagicMock(side_effect=[0, 3])

    genome.mutate_gene(innovations)

    random.choice = old

    assert len(genome.genes) == 7
    assert len(innovations.gene_innov) == 1

def test_mutate_gene_none_free():
    genome = Genome.minimal_fully_connected(0, (3, 2))

    innovations = Innovations()

    innovations.innov = max(map(lambda x: x.innov, genome.genes))

    old = random.choice

    random.choice = mock.MagicMock(side_effect=[0, Genome.MAX_HIDDEN])

    genome.mutate_gene(innovations)

    random.choice = old

    assert len(genome.genes) == 6
    assert len(innovations.gene_innov) == 0

def test_mutate_neuron():
    genome = Genome.minimal_fully_connected(0, (3, 2))

    innovations = Innovations()

    innovations.innov = max(map(lambda x: x.innov, genome.genes))

    genome.mutate_neuron(innovations)

    assert len(genome.genes) == 8
    assert sum(genome.neurons) == 6
    assert len(innovations.neuron_innov) == 1

def test_compatible():
    conf = Conf()

    g1 = Genome.minimal_fully_connected(0, (3, 2))

    g2 = g1.duplicate(1)

    g2.mutate_weights()

    assert g1.compatible(conf, g2)

def test_compatible_diff_struct():
    conf = Conf()
    innovations = Innovations()

    g1 = Genome.minimal_fully_connected(0, (3, 2))

    innovations.innov = max(map(lambda x: x.innov, g1.genes))

    g2 = g1.duplicate(1)

    g2.mutate_neuron(innovations)

    assert not g1.compatible(conf, g2)
