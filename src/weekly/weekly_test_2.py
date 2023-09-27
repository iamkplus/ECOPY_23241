import random
import math

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
        return self.scale * math.log(random.random()) - (self.scale * math.log(random.random()))
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
        self.moments = []
        self.moments.append(0)
        self.moments.append(2 * (self.scale ** 2) + self.loc ** 2)
        self.moments.append(0)
        self.moments.append(24 * (self.scale ** 4))
        return self.moments

class ParetoDistribution:
    def __init__(self, rand, scale, shape):
        self.rand = rand
        self.scale = scale
        self.shape = shape
    def pdf(self, x):
        return (self.shape * (self.scale ** self.shape)) / (x ** (self.shape + 1))
    def cdf(self, x):
        return 1 - ((self.scale / x) ** self.shape)
    def mean(self):
        return (self.shape * self.scale) / (self.shape - 1)

    def variance(self):
        return (self.scale ** 2) * self.shape / (((self.shape - 1) ** 2) * (self.shape - 2))

    def skewness(self):
        return 2 * (1 + self.shape) / (self.shape - 3) * (((self.shape - 2) / self.shape) ** 0.5)