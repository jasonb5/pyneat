import numpy as np

import logging

class RecurrentNeuralNetwork(object):
    """Recurrent Neural Network.

    Attributes:
        dimension: 3-tuple of input, hidden, and output nodes
        act_func: Networks activation function
    """
    def __init__(self, dimension, act_func=None):
        self.dim = dimension
        self.wi = np.zeros((dimension[1], dimension[0]))
        self.wh = np.zeros((dimension[1], dimension[1]))
        self.wo = np.zeros((dimension[2], sum(dimension[:2])))
        self.wb = np.zeros((dimension[1], dimension[2]))

        self.dh = np.zeros((dimension[1], 1))
        self.do = np.zeros((dimension[2], 1))
        
        self.act_func = None

        if act_func:
            self.act_func = np.vectorize(act_func, float)

    def __input(self, node):
        return node >= 0 and node < self.dim[0]

    def __hidden(self, node):
        return node >= self.dim[0] and node < sum(self.dim[:2])

    def __output(self, node):
        return node >= sum(self.dim[:2]) and node < sum(self.dim)

    def __inode(self, node):
        return node

    def __hnode(self, node):
        return node - self.dim[0]

    def __onode(self, node):
        return node - sum(self.dim[:2])

    def add_link(self, inode, onode, weight=1.0):
        """Adds link to network.

        Inserts link from inode to onode with weight. The nodes are indexed
        from 0 to n where n-1 is the sum of input, hidden, and output. For
        example, a link from the first input to the second output of a network
        in the form of (2, 2, 2) would look like add_link(0, 5).

        Args:
            inode: input node index
            onode: output node index
            weight: weight of the link
        """
        if self.__input(inode) and self.__hidden(onode):
            self.wi[self.__hnode(onode), self.__inode(inode)] = weight
        elif self.__input(inode) and self.__output(onode):
            self.wo[self.__onode(onode), self.__inode(inode)] = weight
        elif self.__hidden(inode) and self.__hidden(onode):
            self.wh[self.__hnode(inode), self.__hnode(onode)] = weight
        elif self.__hidden(inode) and self.__output(onode):
            self.wo[self.__onode(onode), self.dim[0]+self.__hnode(inode)] = weight
        elif self.__output(inode) and self.__hidden(onode):
            self.wb[self.__hnode(onode), self.__onode(inode)] =  weight
        else:
            logging.error('Cannot add link from {0} to {1}', inode, onode)

            return False

        return True

    def activate(self, data):
        """Activates the network.

        Peforms one timestep of the network.

        Args:
            data: input data of len(dimension[0])

        Returns:
            A list of output values of len(dimension[2])
        """
        di = np.array(data).reshape((len(data), 1))

        dtemp = np.dot(self.wi, di)+np.dot(self.wh, self.dh)+np.dot(self.wb, self.do)

        if self.act_func:
            self.dh = self.act_func(dtemp)
        else:
            self.dh = dtemp

        dconcat = np.concatenate((di, self.dh))

        self.do = np.dot(self.wo, dconcat)

        if self.act_func:
            self.do = self.act_func(self.do)

        return self.do.squeeze().tolist()
