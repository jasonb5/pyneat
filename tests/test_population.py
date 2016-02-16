from pyneat import Conf
from pyneat import Population
from pyneat.genotype import Genome

def test_population():
    conf = Conf()

    genome = Genome.minimal_fully_connected(0, (3, 2))

    pop = Population(conf)

    pop.spawn(genome)

    assert len(pop.organisms) == conf.pop_size
    assert len(pop.species) == 1
