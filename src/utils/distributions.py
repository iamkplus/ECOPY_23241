import random

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



# innentől képletek
# normál eloszlás:
# átlag = medián
# ferdeség, csúcsosság = 0; centrális momentumokból a második variancia, többi 0

# cauchy: átlag nincs, medián középpont, nincs ferdeség, variancia, csúcsosság, és momentum