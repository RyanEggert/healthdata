import numpy as np
import pandas as pd

import meps.think.stats2 as thinkstats2
import meps.data.dataio as dataio


class DiffMeansPermute(thinkstats2.HypothesisTest):

    """Performs difference-of-means hypothesis test.
    From Allen Downey's "Think Stats 2".
    """

    def TestStatistic(self, data):
        """Calculates test statistic (in this case, difference of means)
                data: tuple containing two datasets (ex. dataframes, lists)
                Returns: float difference in means
        """
        group1, group2 = data
        test_stat = abs(group1.mean() - group2.mean())
        return test_stat

    def MakeModel(self):
        """Creates model for hypothesis test -- combines both groups within
            data to create a pool.
        """
        group1, group2 = self.data
        self.n, self.m = len(group1), len(group2)
        self.pool = np.hstack((group1, group2))

    def RunModel(self):
        """Runs model for hypothesis test -- creates two groups from model
            to form the null hypothesis model.
        """
        np.random.shuffle(self.pool)
        data = self.pool[:self.n], self.pool[self.m:]
        return data


def test_diffmean_hyp(filename, var1, var2):
    """Performs hypothesis test using a dataset from "filename".
        It examines the average difference in "var2" between those for whom
        var1 is true and those for whom var1 is false.

        filename: .pkl file containing the dataset
        var1: variable that divides dataset into two groups (var1 is true,
              var1 is false)
        var2: variable for which the difference in means is calculated
              (var2 mean for group 1 minus
            var2 mean for group 2)

        Returns: dictionary containing size of groups, means,
                 difference in means, p-value
    """
    d = {}

    df = dataio.importdata('h155.pkl')

    cond = df[(df[var1] == 1) & (df[var2] >= 0)]  # group with condition
    nocond = df[(df[var1] == 2) & (df[var2] >= 0)]  # group without condition

    data = cond[var2].values, nocond[var2].values
    hyptest = DiffMeansPermute(data)
    pvalue = hyptest.PValue()

    d['Group Size'] = (hyptest.n, hyptest.m)
    d['Means'] = (data[0].mean(), data[1].mean())
    d['Difference in Mean'] = hyptest.TestStatistic(data)
    d['P-value'] = pvalue

    return d


def main():
    # testing hypothesis
    # var1 = 'EMPHDX'
    # var2 = 'TTLP12X'
    # df = dataio.importdata('h155.pkl')

    # two groups to test
    # cond = df[(df[var1] == 1) & (df.TTLP12X >=0)]   #group with condition
    # nocond = df[(df[var1] == 2) & (df.TTLP12X >=0)] #group without condition

    # performs hypothesis test
    # data = cond.TTLP12X.values, nocond.TTLP12X.values
    # hyptest = DiffMeansPermute(data)
    # pvalue = hyptest.PValue()

    # print "Group size of (cond, nocond): (%d, %d)" %(hyptest.n, hyptest.m)
    # print "Means of (cond, nocond) for variable %s: (%.4f, %.4f)" %(var2, data[0].mean(), data[1].mean())
    # print "Difference of means: %.4f" %hyptest.TestStatistic(data)
    # print "P-value of difference: %.4f" %pvalue

    # hypothesis test function
    print test_diffmean_hyp('h155.pkl', 'EMPHDX', 'TTLP12X')


if __name__ == '__main__':
    main()
