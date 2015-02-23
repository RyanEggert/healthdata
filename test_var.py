import pandas as pd
import dataio


def subgroups(filename, var):
    """ Takes variable from given dataset and determines how large it is, 
    and the size of subgroups/minority groups within that group.

    Only use this function if this is a yes/no variable (i.e. 1 codes for a positive 
        diagnosis, 2 codes for a negative)

        filename: .pkl file containing the dataset
        var: variable in question
    """

    #How many people have this condition?
    df = dataio.importdata(filename)
    cond = df[df[var] == 1]
    print "Number of participants with condition: " + str(len(cond))

    print "DEMOGRAPHIC VARS"
    print "Age Subgroups:"
    print "\tUnder 25: " + str(len(cond[(cond['AGE12X'] < 24) & (cond['AGE12X'] >= 0)]))
    print "\t25-64: " + str(len((cond[(cond['AGE12X'] >= 25) & (cond['AGE12X'] <=65)])))
    print "\tOver 65: " + str(len(cond[cond['AGE12X'] > 65]))

    print "Gender Subgroups:"
    print "\tMale: " + str(len(cond[cond['SEX'] == 1]))
    print "\tFemale: " + str(len(cond[cond['SEX'] == 2]))

    print "Race Subgroups: "
    print "\tWhite: " + str(len(cond[cond.RACEV1X==1]))
    print "\tBlack: " + str(len(cond[cond.RACEV1X==2]))
    print "\tNative American: " + str(len(cond[cond.RACEV1X==3]))
    print "\tAsian: " + str(len(cond[cond.RACEV1X==4]))
    print "\tPacific Islander: " + str(len(cond[cond.RACEV1X==5]))
    print "\tMultiple: " + str(len(cond[cond.RACEV1X==6]))

    print "Marital Status Subgroups: "                          #only applicable if over 16
    print "\tMarried: " + str(len(cond[cond.MARRY12X==1]))
    print "\tWidowed: " + str(len(cond[cond.MARRY12X==2]))
    print "\tDivorced: " + str(len(cond[cond.MARRY12X==3]))
    print "\tSeparated: " + str(len(cond[cond.MARRY12X==4]))
    print "\tNever Married: " + str(len(cond[cond.MARRY12X==5]))

    print "Education"                                           #only applicable if over 16
    print "\tNone: " + str(len(cond[cond.HIDEG==1]))
    print "\tGED: " + str(len(cond[cond.HIDEG==2]))
    print "\tHigh School: " + str(len(cond[cond.HIDEG==3]))
    print "\tBachelor's: " + str(len(cond[cond.HIDEG==4]))
    print "\tMaster's: " + str(len(cond[cond.HIDEG==5]))
    print "\tDoctorate: " + str(len(cond[cond.HIDEG==6]))
    print "\tOther: " + str(len(cond[cond.HIDEG==7]))

    print "Yearly Total Income"
    print "$0-$1k: " + str(len(cond[(cond.TTLP12X >= 0) & (cond.TTLP12X <= 1000)]))
    print "$1k-$5k: " + str(len(cond[(cond.TTLP12X >= 1001) & (cond.TTLP12X <= 5000)]))
    print "$5k-$25k: " + str(len(cond[(cond.TTLP12X >= 5001) & (cond.TTLP12X <= 25000)]))
    print "$25k-$50k: " + str(len(cond[(cond.TTLP12X >= 25001) & (cond.TTLP12X <= 50000)]))
    print "$50k+: " + str(len(cond[(cond.TTLP12X >= 50000)])) 


    print "HEALTH STATUS VARS"
    print "Functional Limitation: " + str(len(cond[(cond.WLK3MO31 == 1) | (cond.WLK3MO53 == 1)]))
    print "Sight Impairment: " + str(len(cond[(cond.VISION42 > 1)]))
    print "Hearing Impairment: " + str(len(cond[cond.HEARNG42 > 1]))

    print "Time Since Last Routine Checkup: "
    print "\t <1 Year: " + str(len(cond[cond.CHECK53==1]))
    print "\t2-3 Years: " + str(len(cond[(cond.CHECK53 >= 2) & (cond.CHECK53 <= 3)]))
    print "\t4+ Years: " + str(len(cond[(cond.CHECK53 >= 4)]))

    print "Body Mass Index"
    print "\tBMI < 18.5: " + str(len(cond[(cond.BMINDX53 >= 5) & (cond.BMINDX53 < 18.5)]))
    print "\tBMI 18.5 - 25: " + str(len(cond[(cond.BMINDX53 >= 18.5) & (cond.BMINDX53 < 25)]))    
    print "\tBMI 25 - 35: " + str(len(cond[(cond.BMINDX53 >= 25) & (cond.BMINDX53 < 35)]))    
    print "\tBMI 35 - 45: " + str(len(cond[(cond.BMINDX53 >= 35) & (cond.BMINDX53 < 45)]))    
    print "\tBMI 45+: " + str(len(cond[(cond.BMINDX53 >= 45)])) 

def main():
    subgroups('h155.pkl', 'ARTHDX')


if __name__ == '__main__':
    main()