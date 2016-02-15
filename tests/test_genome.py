from pyneat.genotype import Genome

def test_genome():
    genome = Genome.minimal_fully_connected((3, 2))

    assert genome.neurons == (3, 0, 2)
    assert len(genome.genes) == 6
