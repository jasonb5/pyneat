from . import Population
from .genotype import Genome

import math
import logging

class Experiment(object):
    """Peforms experiment using NEAT.

    Executes NEAT on a given set of data and a fitness method.

    Fitness method must be a python method named evaluate wrapped in a 
    string. It will have one parameter that will be a list containing the 
    output from the neural networks. Each entry will correspond with the 
    appropriate entry from the data variable passed to the run method.
    The method will need to return a 2-tuple, containing the fitness value
    and whether it is a solution, respectfully.
    
    e.g.

    # Data passed to run method
    data = ((0.0, 0.0, 1.0),
            (1.0, 0.0, 1.0),
            (0.0, 1.0, 1.0),
            (1.0, 1.0, 1.0))

    def evaluate(res):
        winner = False

        error = math.fabs(res[0]+(1-res[1])+(1-res[2])+res[3])

        fitness = math.pow(4-error, 2)

        if res[0] < 0.5 and res[1] >= 0.5 and res[2] >= 0.5 and res[3] < 0.5:
            winner = True

        return fitness, winner

    Attributes:
        name: Name of experiment.
        log: Logger for experiment class.
    """
    def __init__(self, name):
        self.name = name
        self.log = logging.getLogger('experiment')

    def run(self, conf, db=None):
        """Runs experiment.

        Creates a population where each organism evaluates the given data.
        The results are passed to a fitness method the result is assigned
        to that organism. At the end of each generation the populations
        epoch occurs, creating the next generation.

        Args:
            num_input: Number of input neurons.
            num_output: Number of output neurons.
            conf: Instance of Conf class.
            data: N sized array containing num_input-tuples that will be 
                evaluated by the population.
            fitness_func: Fitness method. See class description.
            runs: Number of runs to perform. Defautlts to 1.
        """
        genome = Genome.minimal_fully_connected(0, 
                (conf.num_input, conf.num_output))

        ns = {'math': math}

        exec conf.fitness_func in ns

        db.push_experiment(self.name, conf)

        for r in xrange(conf.runs):
            db.push_population(r)

            pop = Population(conf)

            pop.spawn(genome)

            for g in xrange(conf.generations):
                for o in pop.organisms:
                    winner = False

                    net = o.genome.genesis()

                    res = []

                    for d in conf.data:
                        res.append(net.activate(d))

                    o.fitness, o.winner = ns['evaluate'](res)

                    if o.winner:
                        self.log.info('Winner!!')

                        return

                pop.epoch(db)
