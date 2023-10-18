import random
import math
from scipy.special import gamma, gammainc, gammaincinv
import pyerf

# 1
class FirstClass:
    pass

# 2
class SecondClass:
    def __init__(self, rand):
        self.random = rand

# 3 - 4 - 5 - 6 - 7
class UniformDistribution:
    def __init__(self, rand, a, b):
        self.rand = rand
        self.a = a
        self.b = b
    def pdf(self, x):
        self.pdf = 1 / (self.b - self.a)
        return self.pdf
    def cdf(self, x):
        self.cdf = (x - self.a) / (self.b - self.a)
        return self.cdf
    def ppf(self, x):
        self.ppf = self.a + x * (self.b - self.a)
        return self.ppf
    def gen_rand(self):
        return random.uniform(self.a, self.b)
    def mean(self):
        if (self.b < self.a):
            raise Exception("Moment undefined")
        self.mean = (self.a + self.b)/2
        return self.mean
    def median(self):
        return (self.a + self.b)/2

    def median(self):
        return (self.a + self.b)/2

    def variance(self):
        return (self.b - self.a) / 12

    def skewness(self):
        return 0
    def ex_kurtosis(self):
        return - self.b / (self.b - self.a)

    def mvsk(self):
        self.mvsk = []
        self.mvsk.append(self.mean())
        self.mvsk.append(self.variance())
        self.mvsk.append(self.skewness())
        self.mvsk.append(self.ex_kurtosis())
        return self.mvsk

class NormalDistribution:
    def __init__(self, rand, loc, scale):
        self.rand = rand
        self.loc = loc
        self.scale = scale

    def pdf(self, x):
        std = self.scale ** 0.5
        return (1 / (std * math.sqrt(2 * math.pi))) * math.exp(-((x - self.loc) ** 2) / (2 * std ** 2))

    def cdf(self, x):
        std = self.scale ** 0.5
        return 0.5 * (1 + math.erf((x - self.loc) / (std * math.sqrt(2))))

    def ppf(self, p):
        std = self.scale ** 0.5
        return self.loc + std * math.sqrt(2) * pyerf.erfinv(2 * p - 1)

    def gen_rand(self):
        std = self.scale ** 0.5
        return self.loc + std * math.sqrt(2) * pyerf.erfinv(2 * random.random() - 1)


class LogisticDistribution:
    def __init__(self, rand, loc, scale):
        self.rand = rand
        self.loc = loc
        self.scale = scale

    def pdf(self, x):
        return math.exp(( - (x - self.loc) / self.scale)) / (self.scale * ((1 + math.exp(- (x - self.loc) / self.scale)) ** 2))

    def cdf(self, x):
        return 1 / (1 + math.exp( - (x - self.loc) / self.scale))

    def ppf(self, p):
        return self.loc + self.scale * math.log(p / (1 - p))

    def gen_rand(self):
        p = self.rand
        return self.loc + self.scale * math.log(p / (1 - p))

    def mean(self):
        return self.loc

    def variance(self):
        return ((math.pi ** 2) / 3) * (self.scale ** 2)

    def skewness(self):
        return 0

    def ex_kurtosis(self):
        return 6 / 5

    def mvsk(self):
        moments = []
        moments.append(self.mean())
        moments.append(self.variance())
        moments.append(self.skewness())
        moments.append(self.ex_kurtosis())
        return moments

class ChiSquaredDistribution:
    def __init__(self, rand, dof):
        self.rand = rand
        self.dof = dof

    def pdf(self, x):
        return (1 / (math.pow(2, self.dof / 2) * gamma(self.dof / 2))) * (math.pow(x, self.dof / 2 - 1) * math.exp(- x / 2))

    def cdf(self, x):
        return gammainc(self.dof / 2, x / 2)

    def ppf(self, p):
        return 2 * gammaincinv(self.dof / 2, p)

    def gen_rand(self):
        p = random.random()
        return 2 * gammaincinv(self.dof / 2, p)

    def mean(self):
        return self.dof

    def variance(self):
        return self.dof * 2

    def skewness(self):
        return (8 / self.dof) ** 0.5

    def ex_kurtosis(self):
        return 12 / self.dof

    def mvsk(self):
        moments = []
        moments.append(self.mean())
        moments.append(self.variance())
        moments.append(self.skewness())
        moments.append(self.ex_kurtosis())
        return moments

class CauchyDistribution:
    def __init__(self, rand, loc, scale):
        self.rand = rand
        self.loc = loc
        self.scale = scale

    def ppf(self, p):
        return math.tan(math.pi*p - math.pi/2.0)

    def gen_rand(self):
        p = random.random()
        return math.tan(math.pi * p - math.pi / 2.0)