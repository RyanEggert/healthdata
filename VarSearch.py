
import re
import DataSet


def search_vars(vartype, vars):
    """Searches through a given list of variables and returns
    a list of those that match the specified variable type.

    vartype: string -- type of variable to search for.
             'diagnosis': disease diagnosis variables
             'total expenditure': yearly expenditure variables
             'age of diagnosis': age of diagnosis variables
    vars: A list of variables from the dataset -- list of strings

    Returns: list of matches -- list of strings 
    """
    diag = re.compile('[A-Z]+DX[0-9]*')            #compiles regular expressions to search
    tot_exp = re.compile('TOT[A-Z]+12[0-9]*')
    age_diag = re.compile('[A-Z]+AGED[0-9]*')



    #dictionary containing vartypes and their corresponding compiled regular expressions
    var_types = {'diagnosis': diag, 'total expenditure': tot_exp, 'age of diagnosis': age_diag}

    regexp = var_types[vartype]                #chooses the appropriate regular expression

    var_matches = []                        #list of matches

    for var in vars:                        #iterates through variable list, adds matches to var_matches
        match = regexp.match(var)
        if(match):
            var_matches.append(match.group())

    return var_matches

def main():
    dset = DataSet.DataSet('h155.pkl')        #loads dataset, list of variables in dataset as list of strings
    vars = dset.varnames
    print search_vars('age of diagnosis', vars)       #searches through the HC-155 dataset for age of diagnosis variables


if __name__ == '__main__':
    main()