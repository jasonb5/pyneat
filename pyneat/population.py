from . import Species

class Population(object):
    """Population of organisms.

    Maintains population of organisms for an experiment. Controls the fitness
    sharing, speciation, and repopulation for each generation.

    Attributes:
        conf: instance of Conf class
    """
    def __init__(self, conf):
        self.conf = conf
        self.organisms = []
        self.species = []

    def spawn(self, genome):
        """Spawns initial population

        Creates population from an inital genome, mutating between each
        duplication.

        Args:
            genome: initial genome of the population
        """
        self.neuron = sum(genome.neurons)

        for x in xrange(self.conf.pop_size):
            new_genome = genome.duplicate(x)

            new_genome.mutate_weights()

            self.speciate(new_genome)

            self.organisms.append(new_genome)

    def speciate(self, organism):
        """Speciate organism.

        Search for a compatible species otherwise create a new one.

        Args:
            organism: Organism to be speciated.
        """
        for s in self.species:
            if s.organisms[0].compatible(self.conf, organism):
                s.organisms.append(organism)

                return

        species = Species()

        species.organisms.append(organism)

        self.species.append(species)
