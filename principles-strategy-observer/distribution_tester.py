import random


class DistributionTester:
    def __init__(self, distribution_generator, percentile_calculator) -> None:
        self.distribution_generator = distribution_generator
        self.percentile_calculator = percentile_calculator
        
    def test_distribution(self, p):
        distribution = self.distribution_generator.generate()
        perc_result = self.percentile_calculator.calculate_percentiles(distribution, p)
        
        print(f"Distribution: {distribution}")
        print(f"Percentile {p}: {perc_result}")
        
class SequentialGenerator:
    def __init__(self, start, end, step):
        self.start = start
        self.end = end
        self.step = step
        
    def generate(self):
        return [x for x in range(self.start, self.end + 1, self.step)]
    
class RandomGenerator:
    def __init__(self, mean, sigma, count):
        self.mean = mean
        self.sigma = sigma
        self.count = count
        
    def generate(self):
        return [int(random.gauss(self.mean, self.sigma)) for _ in range(self.count)]
    
class FibonacciGenerator:
    def __init__(self, count):
        self.count = count
        
    def generate(self):
        fib = [0, 1]
        while len(fib) < self.count:
            fib.append(fib[-1] + fib[-2])
        return fib [:self.count]
    
class NearestRankPercentile:
    def calculate_percentiles(self, distribution, p):
        sorted_distribution = sorted(distribution)
        index = round(p / 100 * len(distribution) + 0.5) - 1
        return sorted_distribution[min(index, len(distribution) - 1)]

    
class InterpolatedPercentile():
    def calculate(self, distribution, p):
        sorted_distribution = sorted(distribution)
        N = len(sorted_distribution)
        
        if p <= 100 * (0.5 / N):
            return sorted_distribution[0]
        if p >= 100 * ((N - 0.5) / N):
            return sorted_distribution[-1]
        
        for i in range(1, N):
            p_i = 100 * (i - 0.5) / N
            p_i_plus_1 = 100 * ((i + 1) - 0.5) / N
            
            if p_i < p <= p_i_plus_1:
                v_i = sorted_distribution[i - 1]
                v_i_plus_1 = sorted_distribution[i]
                return v_i + N * (p - p_i) * (v_i_plus_1 - v_i) / 100
    
def test():
    distribution_generator = SequentialGenerator(0, 10, 1)
    percentile_calculator = NearestRankPercentile()
    tester = DistributionTester(distribution_generator=distribution_generator, percentile_calculator=percentile_calculator)
    
    p = 95
    tester.test_distribution(p)
    
if __name__ == "__main__":
    test()