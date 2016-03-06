from . import Organism

import random
import logging

class Species(object):
    """Species of organisms.

    Groups organisms into species. Speciatation is used to prevent getting
    stuck in local maximums by keeping the population diverse. This allows 
    for innovations to mature before being removed from the population. Fitness
    sharing within a species allows for similar strutures to compete with 
    eachother rather than competing with organisms of differing structures. 
    This helps keep the population diverse as well.
    """
    def __init__(self, species_id):
        self.species_id = species_id
        self.organisms = []
        self.max_fitness = 0
        self.avg_fitness = 0
        self.age_since_imp = 0
        self.offspring = 0
        self.marked = False
        self.log = logging.getLogger('species')

    def epoch(self, conf, innovs, num=None):
        """Species epoch.

        During species epoch the next generations children are created.
        The default selection process is rank where the rank determines
        the probability and then a basic roulette wheel is applied.

        Args:
            conf: Instance of Conf class.
            innovs: Instance of Innovations class.

        Retruns: List of new children.
        """
        children = []

        self.organisms.sort(cmp=lambda x, y: cmp(x.rank, y.rank))

        local_ranks = [i for i in xrange(1, len(self.organisms)+1)]

        sum_rank = sum(local_ranks)

        local_probs = [float(i)/float(sum_rank) for i in local_ranks]

        shift_probs = [sum(local_probs[:i+1]) for i in xrange(len(local_probs))]

        pool = zip(shift_probs, self.organisms)

        offspring = num if num else self.offspring-1

        # Produce one less than offspring since the most fit will be passed on
        for x in xrange(offspring):
            if random.random() < conf.mutate_only_prob:
                the_org = self.random_org(pool)

                baby_genome = the_org.genome.duplicate(innovs.next_genome())

                if random.random() < conf.mutate_neuron_prob:
                    self.log.info('genome %d parent %d mutate neuron',
                            baby_genome.genome_id,
                            the_org.genome.genome_id)

                    baby_genome.mutate_neuron(innovs)
                elif random.random() < conf.mutate_gene_prob:
                    self.log.info('genome %d parent %d mutate gene',
                            baby_genome.genome_id,
                            the_org.genome.genome_id)

                    if not baby_genome.mutate_gene(innovs):
                        self.log.error('genome %d gene mutation failed',
                                baby_genome.genome_id)
                else:
                    self.log.info('genome %d parent %d mutate weights',
                            baby_genome.genome_id,
                            the_org.genome.genome_id)

                    baby_genome.mutate_weights(conf.mutate_power, 1.0)
            else:
                mom = self.random_org(pool)
                dad = self.random_org(pool)

                baby_genome = mom.genome.crossover(
                        dad.genome, 
                        mom.fitness, 
                        dad.fitness,
                        innovs)

                self.log.info('genome %d mom %d dad %d',
                        baby_genome.genome_id,
                        mom.genome.genome_id,
                        dad.genome.genome_id)

                # Force mutation after mating if the parents are the same
                # genome or if they're compatible.
                if (mom.genome.genome_id == dad.genome.genome_id or
                        mom.genome.compatible(conf, dad.genome) or
                        random.random() > conf.mate_only_prob):
                    if random.random() < conf.mutate_neuron_prob:
                        self.log.info('genome %d mutate neuron after mate',
                                baby_genome.genome_id)
                        
                        baby_genome.mutate_neuron(innovs)
                    elif random.random() < conf.mutate_gene_prob:
                        self.log.info('genome %d mutate gene after mate',
                                baby_genome.genome_id)

                        if not baby_genome.mutate_gene(innovs):
                            self.log.error('genome %d gene mutation failed',
                                    baby_genome.genome_id)
                    else:
                        self.log.info('genome %d mutate weights after mate',
                                baby_genome.genome_id)

                        baby_genome.mutate_weights(conf.mutate_power, 1.0)

            children.append(Organism(baby_genome))

        return children

    def random_org(self, pool):
        """Selects random organism from pool.

        Runs the roulette wheel to select an organism.

        Args:
            pool: Array of 2-tuple sets where the first item is the probability
                    between 0.0 and 1.0 and the second item is the organism.

        Returns: Selected organism from pool.
        """
        sel = random.random()

        for candidate in pool:
            if sel < candidate[0]:
                return candidate[1]

        return None
