from pyneat import Conf
from pyneat import Innovations
from pyneat.genotype import Genome

import mock
import random

def test_genome():
    genome = Genome.minimal_fully_connected(0, (3, 2))

    assert genome.neurons == [3, 0, 2]
    assert len(genome.genes) == 6

def test_crossover_equal_mom_fit():
    innovs = Innovations()

    mom = Genome.minimal_fully_connected(0, (3, 2))

    dad = mom.duplicate(1)

    baby = mom.crossover(dad, 2.0, 1.0, innovs)

    assert len(baby.genes) == 6

def test_crossover_equal_dad_fit():
    innovs = Innovations()

    mom = Genome.minimal_fully_connected(0, (3, 2))

    dad = mom.duplicate(1)

    baby = mom.crossover(dad, 1.0, 2.0, innovs)

    assert len(baby.genes) == 6

def test_crossover_unequal_mom_mut_dad_fit():
    innovs = Innovations()

    mom = Genome.minimal_fully_connected(0, (3, 2))

    innovs.innov = max(map(lambda x: x.innov, mom.genes))

    dad = mom.duplicate(1)

    mom.mutate_neuron(innovs)

    baby = mom.crossover(dad, 2.0, 1.0, innovs)

    assert len(baby.genes) == 8

def test_crossover_unequal_mom_mut_mom_fit():
    innovs = Innovations()

    mom = Genome.minimal_fully_connected(0, (3, 2))

    innovs.innov = max(map(lambda x: x.innov, mom.genes))

    dad = mom.duplicate(1)

    mom.mutate_neuron(innovs)

    baby = mom.crossover(dad, 1.0, 2.0, innovs)

    assert len(baby.genes) == 6

def test_crossover_unequal_dad_mut_dad_fit():
    innovs = Innovations()

    mom = Genome.minimal_fully_connected(0, (3, 2))

    innovs.innov = max(map(lambda x: x.innov, mom.genes))

    dad = mom.duplicate(1)

    dad.mutate_neuron(innovs)

    baby = mom.crossover(dad, 1.0, 2.0, innovs)

    assert len(baby.genes) == 8

def test_crossover_unequal_dad_mut_mom_fit():
    innovs = Innovations()

    mom = Genome.minimal_fully_connected(0, (3, 2))

    innovs.innov = max(map(lambda x: x.innov, mom.genes))

    dad = mom.duplicate(1)

    dad.mutate_neuron(innovs)

    baby = mom.crossover(dad, 2.0, 1.0, innovs)

    assert len(baby.genes) == 6

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

def test_genesis():
    genome = Genome.minimal_fully_connected(0, (3, 2))

    net = genome.genesis()

    assert net
    assert net.dim == [3, 0, 2]
