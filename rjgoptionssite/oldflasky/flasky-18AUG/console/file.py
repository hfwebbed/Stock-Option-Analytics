import math
import random
import scipy.stats as sct

print(math.sqrt(math.pi / 2 ))

bases = [100,250,400,700,1000,1400]
vuolas = [5,10,15,25,35,50,80]

runs = 10000

for price in bases:
    for volatility in vuolas:
        sum = 0
        for i in range(runs):
            res = math.fabs(sct.norm.ppf(random.random(), price, volatility * 1.25) - price)
            sum += res
        print("let base = ", price, "volatility = ", volatility, ";  avg price change ", sum / runs, "which is ", 100 * (sum / runs) / volatility, "% of volatility")

