from . import Species

import math

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

    def cull_species(self):
        """Culling the species.

        Order the organisms by fitness then trim the lower performing.
        Allowing only the top performing to repopulate the next generation.
        """
        for s in self.species:
            s.organisms.sort(cmp=lambda x, y: cmp(x.fitness, y.fitness),
                    reverse=True)

            survivors = int(math.floor(len(s.organisms)*self.conf.survival_rate))

            del s.organisms[survivors:]

    def epoch(self, generation):
        """Populations epoch.

        The beginning of a new generation. First the low performing organisms
        should be removed. Next the organisms are ranked for the selection. 
        Each species needs to update its age since last improvements so 
        stagnating species can be removed. Species will also need to be
        assigned how many offspring they will contribute to the next 
        generation, if none they will be removed. The top performing from each
        species will automatically move to the next generation. Next 
        reproduction takes place, if there's a gap between the total 
        reproduced and population size, random species will be selected to 
        fill in the gap. All the new organisms need to be speciated and the 
        populations epoch is done.

        Args:
            generation: Current generation.
        """
        self.cull_species()
