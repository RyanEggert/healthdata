def main():
    H152a = DataSet('h152e.pkl')
    df = cleanallerrs(H152a.df)

    print df.ERCCC1X.value_counts()
    print df.ERCCC2X.value_counts()
    print df.ERCCC3X.value_counts()






if __name__ == '__main__':
    from meps.data import DataSet
    from meps.data.cleaning.cleanerrs import cleanerrs, cleanallerrs
    main()
