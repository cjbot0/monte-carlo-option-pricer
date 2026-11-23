import numpy as np


class Gambler: #starts blueprint, use capital letter for class names
    def __init__(self, bankroll): #using __init__ method, self is a reference to the instance of the class, runs automatically when the class is instantiated
        self.bankroll = bankroll #self is used as a placeholder for the instance of the class, bankroll is an attribute of the class

    def win(self, amount): #method to handle winning scenarios
        self.bankroll = self.bankroll + amount

    def lose(self, amount): #method to handle losing scenarios
        self.bankroll = self.bankroll - amount

    def bet(self, f, won):
        if won:
            self.bankroll = self.bankroll * (1 + f)
        else:
            self.bankroll = self.bankroll * (1 - f)


alice = Gambler(100)
alice.bet(0.2,True)
print(alice.bankroll)
alice.bet(0.2,False)
print(alice.bankroll)

class DiceRoll: 
    def __init__(self, sides=6): #default value for sides is 6
        self.sides = sides
        self.products = None #initialize product attribute to None

    def roll(self, n): #method to roll the die n times
        die1 = np.random.randint(1, self.sides + 1, size=n) 
        die2 = np.random.randint(1, self.sides + 1, size=n)
        self.products = die1 * die2 #store the product of the two dice rolls in the product attribute
        return self.products.mean()

    def standard_error(self):
        if self.products is None:
            raise ValueError('Roll die first')
        else: 
            return np.std(self.products) / np.sqrt(len(self.products))
sim = DiceRoll()
sim.roll(10**7)
print(sim.standard_error())
        