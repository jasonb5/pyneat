class Gene(object):
    """Representation of a link in a genome.

    Describes a link in a genome between two neurons. The link can be 
    enabled and disabled.

    Args:
        inode: in node index
        onode: out node index
        weight: weight of link
        innov: innovation id of the link
    """
    def __init__(self, inode, onode, weight, innov):
        self.inode = inode
        self.onode = onode
        self.weight = weight
        self.innov = innov
        self.enabled = True
