import random
import math
from scipy.stats import pareto

class LaplaceDistribution:
    def __init__(self, rand, loc, scale):
        self.rand = rand
        self.loc = loc
        self.scale = scale
    def pdf(self, x):
        self.pdf = 1 / (2 * self.scale) * math.exp(- (abs(x - self.loc) / self.scale))
        return self.pdf
    def cdf(self, x):
        return 0.5 + 0.5 * math.copysign(1, (x - self.loc)) * (1 - math.exp(- (abs(x-self.loc) / self.scale)))
    def ppf(self, x):
        return self.loc - self.scale * math.copysign(1, (x - 0.5)) * math.log(1 - 2 * abs(x - 0.5))
    def gen_rand(self):
        u = random.random() - 0.5
        return self.loc - self.scale * math.copysign(1, u) * math.log(1 - 2 * abs(u))
    def mean(self):
        if (self.loc == None):
            raise Exception("Moment undefined")
        else:
            return self.loc
    def variance(self):
        return 2 * (self.scale ** 2)

    def skewness(self):
        return 0
    def ex_kurtosis(self):
        return 3

    def mvsk(self):
        moments = []
        moments.append(self.loc)
        moments.append(2 * (self.scale ** 2))
        moments.append(0)
        moments.append(self.ex_kurtosis())
        return moments

class ParetoDistribution:
    def __init__(self, rand, scale, shape):
        self.rand = rand
        self.scale = scale
        self.shape = shape
    def pdf(self, x):
        return (self.shape * (self.scale ** self.shape)) / (x ** (self.shape + 1))
    def cdf(self, x):
        return 1 - ((self.scale / x) ** self.shape)

    def ppf(self, x):
        return self.scale * math.pow(1 - x, -1 / self.shape)
    def mean(self):
            return (self.scale * self.shape / (self.shape - 1))

    def variance(self):
        if self.shape <= 2:
            raise Exception("Moment undefined")
        else:
            return (self.scale ** 2 * self.shape / ((self.shape - 1) ** 2 * (self.shape - 2)))

    def skewness(self):
        if self.shape <= 3:
            raise Exception("Moment undefined")
        else:
            return ((2 * (1 + self.shape)) / (self.shape - 3)) * (math.pow((1 - (2 / self.shape)), 0.5))

    def ex_kurtosis(self):
        return (6 * (self.shape ** 3 + self.shape ** 2 - 6 * self.shape - 2)) / (self.shape * (self.shape - 3) * (self.shape - 4))

    def fake_ex_kurtosis(self):
        if self.shape <= 4:
            raise Exception("Moment undefined")
        else:
            return (3 * (self.shape - 2) * (3 * (self.shape ** 2) + self.shape + 2)) / (self.shape * (self.shape - 3) * (self.shape - 4))

    def gen_rand(self):
        u = random.random()
        return self.scale * math.pow(1 - u, -1 / self.shape)

    def mvsk(self):
        moments = []
        moments.append(self.mean())
        moments.append(self.variance())
        moments.append(self.skewness())
        moments.append(self.ex_kurtosis())
        return moments