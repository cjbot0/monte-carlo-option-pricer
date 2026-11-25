import numpy as np
import matplotlib.pyplot as plt
ln = np.log

class KellySimulator:
    def __init__(self, p, b):
        self.p = p
        self.b = b
        self.bankroll = None

    def kelly_fraction(self):
        f = ((self.b * self.p - (1 - self.p)) / self.b)
        return f

    def simulate(self, f, n_paths, n_bets):
        wins = np.random.random(size=(n_paths, n_bets)) < self.p
        factors = np.where(wins, 1 + self.b * f, 1 - f) #if win, multiply by 1 + b*f, if loss by 1 - f
        self.bankroll = np.cumprod(factors, axis = 1)

    def median_final(self):
        if self.bankroll is None:
            raise ValueError('Call simulate first')
        return np.median(self.bankroll[:, -1])

    def growth_rate(self, f):
        return self.p * ln(1 + self.b * f) + (1 - self.p) * ln(1 - f)

k = KellySimulator(0.55, 1)
print('Kelly fraction:', k.kelly_fraction())

for f in [0.02, 0.05, 0.1, 0.2, 0.5]:
    k.simulate(f, 10**4, 10**3)
    print(f, k.median_final(), np.exp(1000 * k.growth_rate(f)))

fs = np.linspace(0.002, 0.5, 500)
plt.plot(fs, k.growth_rate(fs))
plt.axhline(0, color = 'k')
plt.axvline(k.kelly_fraction(), color = 'r', linestyle = '--', label = 'Kelly fraction')
plt.xlabel('Fraction of bankroll bet (f)')
plt.ylabel('Log growth per bet')
plt.title(f'Kelly growth curve (p = {k.p}), b = {k.b})')
plt.legend()
plt.savefig('kelly_growth.png')
plt.show()