import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm 
ln = np.log

class PricePaths:
    def __init__(self, s0, mu, sigma):
        self.s0 = s0 #starting price
        self.mu = mu #drift - average yearly growth
        self.sigma = sigma #volatilty - size of the yearly wobble
        self.paths = None #filleed in later by method

    def generate(self, n_paths, n_steps, T):
        dt = T / n_steps
        z = np.random.normal(0, 1, size = (n_paths, n_steps))
        log_returns = (self.mu - 0.5 * self.sigma ** 2) * dt + self.sigma * np.sqrt(dt) * z
        self.paths = self.s0 * np.exp(np.cumsum(log_returns, axis = 1))

    def price_call(self, K, T): #when pricing self.mu is the risk free rate r
        if self.paths is None:
            raise ValueError('Call Generate() first')
        payoffs = np.maximum(self.paths[:, -1] - K, 0)
        return np.exp(-self.mu * T) * payoffs.mean()

def black_scholes_call(S, K, r, sigma, T):
    d1 = ((ln(S / K) + (r + (sigma ** 2 / 2)) * T) / (sigma * np.sqrt(T)))
    d2 = d1 - (sigma * np.sqrt(T))
    c = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return c 
    
p = PricePaths(100, 0.05, 0.2)
bs = black_scholes_call(100, 100, 0.05, 0.2, 1)
sizes = [10 ** 2, 10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7]
p.generate(10 ** 6, 1, 1)
payoffs = np.exp(-p.mu * 1) * np.maximum(p.paths[:, -1] - 100, 0)
price = payoffs.mean()
error = payoffs.std() / np.sqrt(len(payoffs))  # standard error
mean_errors = []

for n in sizes:
    errors = []
    for _ in range(20):
        p.generate(n, 1, 1)
        errors.append(abs(p.price_call(100, 1) - bs))
    mean_errors.append(np.mean(errors))

text = (f"Monte Carlo price: {price:.4f} +/- {error:.4f}\n"
        f"Black-Scholes price: {bs:.4f}\n"
        f"Payoff std (sigma): {payoffs.std():.2f}\n")
print(text)

with open("results.txt", "w") as f:
    f.write(text)

sizes = np.array(sizes)
plt.plot(sizes, mean_errors, 'o-', label='simulation error')
plt.plot(sizes, 14 / np.sqrt(sizes), 'r--', label='14/sqrt(n) (theory)')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of Paths')
plt.ylabel('Mean absolute error')
plt.title('Monte Carlo Price Convergence')
plt.legend()
plt.savefig('convergence_price_paths.png')
plt.show()