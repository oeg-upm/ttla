from collections import Counter
import math


#1. Here we identify four kinds of nominal numbers:
#1.1) sequential
#1.2) hierarchical/compositional?
#1.3) categorical
#1.4) random
#2. Ordinal
#3. Ratio and Interval

do we assume the list is always ordered/sorted?
[sequential]


class Detection(object):

    def __init__(self, values):
        self.values = values


    def is_sequential(self):
        """
        we can detect it by taking the minimum (700) and compare it with a gener-
        ated sequence starting from that minimum value until the maximum (932). It becomes tricky when we have
        missing values due to the selected population having something in common (e.g., sequences of solider for a
        sub-unit). The intuition that we follow is that if more than the square root of the numbers in the generated
        sequence Y are also in the original collection of numbers, then we consider the collection of numbers as a
        sequential collection.
        """
        pass

    def is_hierarchical(self):
        """
        In order to detect hierarchical data in a column we first check the
        number of digits, if it is the same in all the cells, then
        we check if it is not sequential then we consider it to be
        hierarchical. This is if the values are unique; have duplicate values is
        a stron evdence of a non-hierarchical numbers.
        """
        pass

    def is_categorical(self):
        """
        if the given column is categorical or not
        :param col: pandas series
        :return: true of false
        """
        cc = Counter(self.values)
        if len(cc.keys()) <= math.sqrt(len(col)):
            return True
        return False

    def is_nominalRandom(self):
        """
        if this and not sequential, hierarchical or categorical than it is is_nominalRando
        """
        pass

    def is_ordinal(self):
        """
        list of a natural numbers starting from 1 until the last element of the list. An in-
        tuitive way to detect is to see if the set of numbers (what we want to examine) is equal to
        that list of numbers that we generated from 1 until the size of the list.
        no negative and no floats
        """
        pass

    def is_ratioInterval(self):
        """
        positive by nature and they do not have factions. Often have the difference between the square root for the
        maximum number and minimum number in the collection of numbers X is more that 1^10.
        """
        pass
