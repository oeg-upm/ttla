from collections import Counter
import math

"""
Questions:
1) where we should add a contidion that numbers cennot be negative or have to be real;
we dont check that now; not sure for which cases it is necessary now
2) should this be sequential? [0,2,4,6,9,12,15]
3) in hierarchical do all values have to be unique or like 80%? same in other cases, where it is
necessary and what is the treshold for that?
4) in hierarchical do all numbers have to have the same number of digits or like 80%?
5) in sequential how many of values have to have the same difference? currently (int(len(diffs)/2))
6) what should be with [1,1,1,1,1,1] or [2,2,2,2,2,2]
7) hierarchical now has that 80% of values have to have the same length - could be changed
8) i dont fully understand when something with positive and real values would not get to ratiointerval case -
is that okay that in all cases it will fall there? there is a really likaly there will be a lot of random crap there
9) should this be [1,1,3,3,3,3,3,5] categorical or ratiointerval?
"""
class Detection(object):

    def __init__(self, values):
        self.values = values
        self.cleanValues = self.preprocessing()
        self.type = self.getType()


    """ function for cleaning the column """
    def preprocessing(self):
        return self.values

    def getType(self):

        if self.is_ordinal():
            return 'ordinal'
        elif self.is_categorical():
            return 'categorical'
        elif self.is_sequential():
            return 'sequential'
        elif self.is_hierarchical():
            return 'hierarchical'
        elif self.is_ratiointerval():
            return 'ratiointerval'
        else:
            return 'unknown'


    def is_ordinal(self):
        diffs = [j-i for i, j in zip(self.cleanValues[:-1], self.cleanValues[1:])]
        if all(x == diffs[0] for x in diffs) and self.cleanValues[0] == 1:
            return True
        return False

    def is_categorical(self):
        """
        if the given column is categorical or not
        :param col: pandas series
        :return: true of false
        """
        cc = Counter(self.cleanValues)
        if len(cc.keys()) <= math.sqrt(len(self.cleanValues)):
            return True
        return False

    def is_sequential(self):
        """
        diffs: difference between every two consecutive numbers
        mostPopular: the most popular number in diffs
        true if mostPopular value appears in diffs more or equal times than (int(len(diffs)/2)
        also mostPopular cannot be equal to zero
        """
        diffs = [j-i for i, j in zip(self.cleanValues[:-1], self.cleanValues[1:])]
        mostPopular = max(set(diffs), key = diffs.count)
        if diffs.count(mostPopular) >= (int(len(diffs)/2)) and mostPopular != 0:
            return True
        return False

    def is_hierarchical(self):
        """
        In order to detect hierarchical data in a column we first check the
        number of digits, if it is the same in all the cells, then
        we check if it is not sequential then we consider it to be
        hierarchical. This is if the values are unique; have duplicate values is
        a stron evdence of a non-hierarchical numbers.
        """
        lengths = []
        for i in self.cleanValues:
            lengths.append(len(str(i)))
        mostPopular = max(set(lengths), key = lengths.count)
        if lengths.count(mostPopular) >= (int(len(lengths)*0.8)):
            seen = set()
            if not any(i in seen or seen.add(i) for i in self.cleanValues):
                return True
        return False


    #def is_nominalrandom(self):
    #    """
    #    if this and not sequential, hierarchical or categorical than it is is_nominalrandom
    #    """
    #    pass


    def is_ratiointerval(self):
        nonnegative = sum(1 for number in self.cleanValues if number >= 0)
        if len(self.cleanValues) == nonnegative:
            if all(isinstance(x, int) for x in self.cleanValues):
                if (math.sqrt(max(self.cleanValues)) - math.sqrt(min(self.cleanValues))) > 1:
                    return True
        return False
