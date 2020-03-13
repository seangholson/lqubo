import numpy as np
from switch_networks.network_instance_data import *


def swap(input_list, switch):
    """
    Given an input list and a tuple of indices, the indexed list elements are swapped.
    """
    input_list[switch[1]], input_list[switch[0]] = input_list[switch[0]], input_list[switch[1]]
    return input_list


class PermutationNetwork:

    def __init__(self, n):
        """
        A permutation network is a sequence of configurable switches and fixed swaps.
        These are grouped into 'stages' of various sizes (a stage is a consecutive sequence of
        switches/swaps), which alternate
        n: size of the network input
        switches: a list of 'stages'
        swaps: a list of 'stages'
            stage: a list of a switches

        When you instantiate a permutation network with an arbitrary input size n,
        it searches the network_instance_data dict for the network of size n <= k=2^m
        """
        self.n = n                              # This is the input size
        self.k = int(2**np.ceil(np.log2(n)))    # This is the network input size
        self.switch_stages = permutation_network_data.get(self.k, dict()).get('switch_stages')
        self.swap_stages = permutation_network_data.get(self.k, dict()).get('swap_stages')
        self.depth = sum([len(stage) for stage in self.switch_stages])

    def permute(self, config):
        """
        Given an input binary list of length self.depth representing an on/off configuration of the switches
        in self.switches, this method permutes the identity permutation according to the switch network.
        :param config: a binary list of length self.depth
        :return: the corresponding permutation of range(self.n)
        """
        p = list(range(self.k))
        switch_index = 0
        for switch_stage, swap_stage in zip(self.switch_stages, self.swap_stages):
            for switch in switch_stage:
                if config[switch_index]:
                    p = swap(p, switch)
                switch_index += 1
            for switch in swap_stage:
                p = swap(p, switch)
        # Since the full list of k items is permuted, the return result should be pared down
        # to only include the input size n:
        return [item for item in p if item < self.n]


class SortingNetwork:
    """
    A switch network is a sequence of comparators between 2 values.

    When a network is run 'forward', it takes an arbitrary permutation of n values and returns them in
    sorted order.

    When a network is run 'backward', it takes an on/off configuration list of its switches and permutes
    the identity accordingly.
    """

    def __init__(self, n):
        """
        n: size of the network input
        switches: list from switch_list dict
        depth: total number of switches
        """
        self.n = n
        self.switches = sorting_network_data.get(n)
        if self.switches:
            self.depth = len(self.switches)
        else:
            self.depth = np.inf

    def sort(self, p):
        """
        Given an input permutation of size self.depth, this method sorts the permutation.
        The output here should always be range(self.n) for functional sorting networks.
        """
        for switch in self.switches:
            if p[switch[0]] > p[switch[1]]:
                p = swap(p, switch)
        return p

    def sort_config(self, p):
        """
        Given an input permutation of size self.depth, this method sorts the permutation.
        The output here should always be range(self.n) for functional sorting networks.
        """
        config = []
        for switch in self.switches:
            if p[switch[0]] > p[switch[1]]:
                config.append(1)
                p = swap(p, switch)
            else:
                config.append(0)
        return config

    # this is the temporary permute function
    def permute(self, config):
        """
        Given an input binary list of length self.n representing an on/off configuration of the switches
        in self.switches, this method permutes the identity permutation according to the switch network.
        :param config: a binary list of length self.depth
        :return: the corresponding permutation of range(self.n)
        """

        p = list(range(self.n))
        for i, switch in enumerate(self.switches):
            if config[i]:
                p = swap(p, switch)
        return p
