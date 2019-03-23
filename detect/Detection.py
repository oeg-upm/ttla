from collections import Counter
import math
from commons import CATEGORICAL, ORDINAL, SEQUENTIAL, RATIO_INTERVAL, HIERARCHICAL, COUNTS
import logging
from commons.logger import set_config

logger = set_config(logging.getLogger(__name__))


"""
Questions:
1) where we should add a contidion that numbers cennot be negative or have to be real;
we dont check that now; not sure for which cases it is necessary now
Answer: I added that in the categorical, and it should be added to the sequencial as well
2) should this be sequential? [0,2,4,6,9,12,15]
Answer: This looks like a simple counts to me. 
3) in hierarchical do all values have to be unique or like 80%? same in other cases, where it is
necessary and what is the treshold for that?
Answer: I think Hierarchical can be labeled if they are from the same source (within the same range and have the 
same number of digits)
4) in hierarchical do all numbers have to have the same number of digits or like 80%?
Answer: All of them (we assume the data is clean in a way) if not, it should be much higher like 99% and less than 10 items
5) in sequential how many of values have to have the same difference? currently (int(len(diffs)/2))
Answer: I would say the majority, but maybe we need to look at the data to have a more scientific argument
6) what should be with [1,1,1,1,1,1] or [2,2,2,2,2,2]
Answer: this should be ignored
7) hierarchical now has that 80% of values have to have the same length - could be changed
Answer: let us make it a much, and have a table in the paper about the pros and cons for each.
8) i dont fully understand when something with positive and real values would not get to ratiointerval case -
is that okay that in all cases it will fall there? there is a really likaly there will be a lot of random crap there
Answer: Yes, ratio-interval-other would have a lot of crap as a result. Because we are not able to detect random nominals
9) should this be [1,1,3,3,3,3,3,5] categorical or ratiointerval?
This should be categorical. We need to have a formula to balance when it. We could have a formula based on the 
minimum number of values in a numeric property. I think this could be done. 
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
            return ORDINAL
        elif self.is_categorical():
            return CATEGORICAL
        elif self.is_sequential():
            return SEQUENTIAL
        elif self.is_hierarchical():
            return HIERARCHICAL
        else:
            return RATIO_INTERVAL
        # elif self.is_ratiointerval():
        #     return RATIO_INTERVAL
        # else:
        #     return 'unknown'

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
        if len(cc.keys()) <= len(self.cleanValues)**(1/1.5):
            for k in cc.keys():
                if k < 0 or not self.is_int(k):
                    logger.debug("Not categorical because the value is: %s" % (str(k)))
                    return False
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
        mostPopular = max(set(diffs), key=diffs.count)
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
        if lengths.count(mostPopular) >= (int(len(lengths)*0.99)):
            seen = set()
            if not any(i in seen or seen.add(i) for i in self.cleanValues):
                return True
        return False

    # def is_ratiointerval(self):
    #     nonnegative = sum(1 for number in self.cleanValues if number >= 0)
    #     if len(self.cleanValues) == nonnegative:
    #         if all(isinstance(x, int) for x in self.cleanValues):
    #             if (math.sqrt(max(self.cleanValues)) - math.sqrt(min(self.cleanValues))) > 1:
    #                 return True
    #     return False

    def is_count(self):
        """
        Check if the it represents simple counts
        :return:
        """
        

    def is_int(self, num):
        return num-int(num) == 0




def get_num_kind(nums):
    """
    This is used as a wrapper to be called by other models
    :param nums:
    :return:
    """
    d = Detection(nums)
    num_kind = d.getType()
    del d
    return num_kind