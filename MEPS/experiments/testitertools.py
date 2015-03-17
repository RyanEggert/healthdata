from __future__ import print_function
from itertools import product
from numpy.random import choice
a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
b = ['a', 'b', 'c', 'd']


# for i, (x, y) in enumerate(product(a, b)):
#     print(i, x, y)
results = []
for i in xrange(100):
    counter = 0
    you = [1, 1, 1, 1, 1]
    a = [1, 1, 1, 1, 5]
    winner = [5, 5, 5, 5, 5]
    while you != winner:
        counter += 1
        youa = choice(a, len(a), replace=True)
        you = youa.tolist()
    results.append(counter)
print(results)
print(min(results))
