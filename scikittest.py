import numpy as np
from sklearn import datasets

# from matplotlib import pyplot as plt
import pylab as pl

# Split data into training and testing groups
diabetes = datasets.load_diabetes()
diabetes_X_train = diabetes.data[:-20]
diabetes_X_test  = diabetes.data[-20:]
diabetes_y_train = diabetes.target[:-20]
diabetes_y_test  = diabetes.target[-20:]

## Linear regression ##

from sklearn import linear_model
regr = linear_model.LinearRegression()
regr.fit(diabetes_X_train, diabetes_y_train)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean square error
print("Residual sum of squares: %.2f"
      % np.mean((regr.predict(diabetes_X_test) - diabetes_y_test) ** 2))
# Explained variance score: 1 is perfect prediction
# and 0 means that there is no linear relationship
# between X and Y.
print('Variance score: %.2f' % regr.score(diabetes_X_test, diabetes_y_test))
