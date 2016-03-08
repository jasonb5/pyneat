import os 
import sys
import django

sys.path.append('../pyneat-web')
os.environ['DJANGO_SETTINGS_MODULE'] = 'pyneat_web.settings'

from pyneat_web import settings

settings.DATABASES['default']['HOST'] = '127.0.0.1'

django.setup()

from neatweb import models

class Database(object):
    def __init__(self):
        self.exp = None
        self.pop = None
        self.gen = None

    def push_experiment(self, name, conf):
        self.exp = models.Experiment(
                name=name,
                config=conf.to_json())

        self.exp.save()

    def push_population(self, rel_index):
        self.pop = models.Population(
                rel_index=rel_index,
                experiment=self.exp)

        self.pop.save()

    def push_generation(self, rel_index, species):
        self.gen = models.Generation(
                rel_index=rel_index,
                population=self.pop)

        self.gen.save()

        organisms = []

        for s in species:
            species = models.Species(
                    rel_index=s.species_id,
                    marked=s.marked,
                    avg_fitness=s.avg_fitness,
                    max_fitness=s.max_fitness,
                    offspring=s.offspring,
                    age_since_imp=s.age_since_imp,
                    population = self.pop,
                    generation = self.gen)

            species.save()

            for o in s.organisms:
                org = models.Organism(
                        rel_index=o.genome.genome_id,
                        winner=o.winner,
                        marked=o.marked,
                        fitness=o.fitness,
                        rank=o.rank,
                        species=species,
                        generation=self.gen,
                        population=self.pop)

                organisms.append(org)

        models.Organism.objects.bulk_create(organisms)
