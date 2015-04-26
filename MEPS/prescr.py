def main():
    H152a = DataSet('h152a.pkl')
    df = cleanallerrs(H152a.df)

    print df.RXNAME.value_counts()





if __name__ == '__main__':
    from meps.data import DataSet
    from meps.data.cleaning.cleanerrs import cleanerrs, cleanallerrs
    main()
