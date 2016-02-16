class Species(object):
    """Species of organisms.

    Groups organisms into species. Speciatation is used to prevent getting
    stuck in local maximums by keeping the population diverse. This allows 
    for innovations to mature before being removed from the population. Fitness
    sharing within a species allows for similar strutures to compete with 
    eachother rather than competing with organisms of differing structures. 
    This helps keep the population diverse as well.
    """
    def __init__(self):
        self.organisms = []
