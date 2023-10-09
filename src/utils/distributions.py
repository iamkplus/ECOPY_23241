import random
import math
from scipy.special import gamma, gammainc, gammaincinv
from scipy.stats import chi2

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
        if (self.b < self.a):
            raise Exception("Moment undefined")
        self.median = (self.a + self.b)/2
        return self.median

    def median(self):
        if (self.b < self.a):
            raise Exception("Moment undefined")
        self.median = (self.a + self.b)/2
        return self.median

    def variance(self):
        if (self.b < self.a):
            raise Exception("Moment undefined")
        self.variance = ((self.b - self.a) ** 2) / 12
        return self.variance

    def skewness(self):
        if (self.b < self.a):
            raise Exception("Moment undefined")
        self.skewness = 0
        return self.skewness

    def ex_kurtosis(self):
        if (self.b < self.a):
            raise Exception("Moment undefined")
        self.ex_kurtosis = -1.2
        return self.ex_kurtosis

    def mvsk(self):
        self.mvsk = []
        self.mvsk.append(0)
        self.mvsk.append(self.variance())
        self.mvsk.append(self.skewness())
        self.mvsk.append(self.ex_kurtosis())
        return self.mvsk

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