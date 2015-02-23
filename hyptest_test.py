import thinkstats2
import numpy as np
import pandas as pd
import dataio


class DiffMeansPermute(thinkstats2.HypothesisTest):
    """Performs difference-of-means hypothesis test. 
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


def main():
    var1 = 'EMPHDX'
    var2 = 'TTLP12X'
    df = dataio.importdata('h155.pkl')
    #df = df[df.TTLP12X >=0]

    cond = df[(df[var1] == 1) & (df.TTLP12X >=0)]
    nocond = df[(df[var1] == 2) & (df.TTLP12X >=0)]


    #data = cond[cond.TTLP12X >= 0], nocond[nocond.TTLP12X >= 0]
    data = cond.TTLP12X.values, nocond.TTLP12X.values
    hyptest = DiffMeansPermute(data)
    pvalue = hyptest.PValue()
    print pvalue
    print hyptest.TestStatistic(data)
    print data[0].mean(), data[1].mean()


if __name__ == '__main__':
    main()