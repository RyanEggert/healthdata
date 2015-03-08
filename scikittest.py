from __future__ import print_function
import numpy as np
from sklearn import datasets

import pylab as pl
from sklearn.metrics import mean_squared_error
from sklearn import linear_model
from texttable import Texttable

# Inspiration and guidance from  --
#   http://scikit-learn.org/stable/tutorial/statistical_inference/supervised_learning.html
#   http://scikit-learn.org/0.15/auto_examples/linear_model/plot_ols.html


def prepareTable(cols):
    """Prepares and returns a text table for data writing.
    The table's columns will be center aligned (horizontally and
    vertically)
    cols: number of columns in text table.
    """
    table = Texttable()
    table.set_cols_align(cols * ['c'])
    table.set_cols_valign(cols * ['c'])
    return table


# Split data into training and testing groups
diabetes = datasets.load_diabetes()
diabetes_X_train = diabetes.data[:-20]
diabetes_X_test = diabetes.data[-20:]
diabetes_y_train = diabetes.target[:-20]
diabetes_y_test = diabetes.target[-20:]

# Linear regression #
print('------------------------- Linear Regression -------------------------')
regr = linear_model.LinearRegression()
regr.fit(diabetes_X_train, diabetes_y_train)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean square error
print("Residual sum of squares: %.2f"
      % np.mean((regr.predict(diabetes_X_test) - diabetes_y_test) ** 2))
# Alternative MSE
mse = mean_squared_error(
    diabetes_y_test, regr.predict(diabetes_X_test), sample_weight=None)
print("RMSE: %.4f"
      % np.sqrt(mse))
# Explained variance score: 1 is perfect prediction
# and 0 means that there is no linear relationship
# between X and Y.
print('Variance score: %.2f' % regr.score(diabetes_X_test, diabetes_y_test))

# Ridge regression #
print('------------------------- Ridge Regression --------------------------')
ridregr = linear_model.Ridge(alpha=.1)
ridregr.fit(diabetes_X_train, diabetes_y_train)

# The coefficients
print('Coefficients: \n', ridregr.coef_)
# The mean square error
print("Residual sum of squares: %.2f"
      % np.mean((ridregr.predict(diabetes_X_test) - diabetes_y_test) ** 2))
# Explained variance score: 1 is perfect prediction
# and 0 means that there is no linear relationship
# between X and Y.
print('Variance score: %.2f' % ridregr.score(diabetes_X_test, diabetes_y_test))
print('\n', ' - - - - - - Effect of alpha - - - - - -')
alphas = np.logspace(-6, 1, 10)
alpha_res = [['alpha', 'RMSE', 'Score']]
for alpha in alphas:
    # Note how you can chain regression methods
    ridregr.set_params(alpha=alpha).fit(diabetes_X_train, diabetes_y_train)
    mse = mean_squared_error(diabetes_y_test, ridregr.predict(diabetes_X_test))
    score = ridregr.score(diabetes_X_test, diabetes_y_test)
    alpha_res.append([alpha, np.sqrt(mse), score])


alpha_table = prepareTable(3)
alpha_table.set_cols_dtype(['e', 'e', 'f'])
alpha_table.set_precision(6)
alpha_table.add_rows(alpha_res)
print(alpha_table.draw())
print()

# LASSO regression #
print('------------------------- LASSO Regression --------------------------')
lasregr = linear_model.Lasso()
scores = [lasregr.set_params(alpha=alpha
                             ).fit(diabetes_X_train, diabetes_y_train
                                   ).score(diabetes_X_test, diabetes_y_test)
          for alpha in alphas]
best_alpha = alphas[scores.index(max(scores))]
lasregr.alpha = best_alpha
lasregr.fit(diabetes_X_train, diabetes_y_train)
# The coefficients
print('Coefficients: \n', lasregr.coef_)
# The mean square error
print("Residual sum of squares: %.2f"
      % np.mean((lasregr.predict(diabetes_X_test) - diabetes_y_test) ** 2))
# Explained variance score: 1 is perfect prediction
# and 0 means that there is no linear relationship
# between X and Y.
print('Variance score: %.2f' % lasregr.score(diabetes_X_test, diabetes_y_test))
