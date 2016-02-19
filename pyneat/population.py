from . import Species
from . import Organism
from . import Innovations

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
        self.innovs = Innovations()

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

            org = Organism(new_genome)

            self.speciate(org)

            self.organisms.append(org)

    def speciate(self, organism):
        """Speciate organism.

        Search for a compatible species otherwise create a new one.

        Args:
            organism: Organism to be speciated.
        """
        for s in self.species:
            o = s.organisms[0]

            if o.genome.compatible(self.conf, organism.genome):
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

    def rank(self):
        """Ranks organisms globally.

        Builds temporary list of potential parents then ranks them globally
        where the least fit receive a smaller rank than the most fit.
        """
        parents = []

        for s in self.species:
            parents += s.organisms

        parents.sort(cmp=lambda x, y: cmp(x.fitness, y.fitness))

        for p in xrange(len(parents)):
            parents[p].rank = p+1

    def remove_stagnating_species(self):
        """Remove stagnating species.

        Updates a species max_fitness, ages the species if no improvement has
        occurred and removes species older than the stagnation threshold.
        """
        survivors = []

        for s in self.species:
            imp = False    

            for o in s.organisms:
                if o.fitness > s.max_fitness:
                    imp = True

                    s.max_fitness = o.fitness

                    s.age_since_imp = 0

            if not imp:
                s.age_since_imp += 1

            if s.age_since_imp < self.conf.stagnation_threshold:
                survivors.append(s)

        self.species = survivors

    def remove_weak_species(self):
        """Removes weak species.
        
        Calculates the average fitness for each species then assigns their 
        portion of the next generation. The proportionality is based on 
        their contribution to the populations overall fitness. 
        """
        total_avg_fitness = 0.0

        for s in self.species:
            total = sum(map(lambda x: x.rank, s.organisms))

            s.avg_fitness = float(total)/float(len(s.organisms))

            total_avg_fitness += s.avg_fitness

        survivors = []

        for s in self.species:
            s.offspring = int(math.floor(
                    (s.avg_fitness*self.conf.pop_size/total_avg_fitness)))

            if s.offspring > 0:
                survivors.append(s)

        self.species = survivors

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

        self.rank()

        self.remove_stagnating_species()

        self.remove_weak_species()

        children = []

        for s in self.species:
            children += s.epoch(self.conf, self.innovs)

            del s.organisms[1:]

        for c in children:
            self.speciate(c)

        del self.organisms[:]

        self.organisms = sum(map(lambda x: x.organisms, self.species), [])
