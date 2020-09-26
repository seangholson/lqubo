import numpy as np


class NextPerm:

    def __init__(self,
                 lqubo_result=None,
                 current_perm=None):

        self.lqubo_result = lqubo_result
        self.current_perm = current_perm

    @staticmethod
    def swap(input_list, entry):
        input_list[0], input_list[entry] = input_list[entry], input_list[0]
        return input_list

    def next_perm(self):
        new_perm = self.current_perm.copy()
        for index in range(len(self.lqubo_result)):
            entry = self.lqubo_result[index]
            if entry == 1:
                new_perm = self.swap(new_perm, index + 1)

        return new_perm




