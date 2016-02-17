from pyneat import Conf
from pyneat import Species
from pyneat import Innovations
from pyneat import Organism
from pyneat.genotype import Genome

import random

def test_reproduce():
    conf = Conf()

    innovs = Innovations()

    genome = Genome.minimal_fully_connected(0, (2, 3))

    species = Species()

    ranks = random.sample(xrange(20), 10)

    for x in xrange(10):
        new_genome = genome.duplicate(innovs.next_genome())

        org = Organism(new_genome)

        org.rank = ranks[x]

        species.organisms.append(org)

    species.offspring = 10

    children = species.epoch(conf, innovs)

    assert len(children) == 10
