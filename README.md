# Monte Carlo Option Pricer 

Vectorized Monte Carlo pricing engine for European options, checked using the Black-Scholes Formula

## What it does

Using geometric Brownian motion, stock prices are simulated, and prices a European call as the discounted average payoff. Then validates the results against the Black-Scholes formula. Fully vectorized with NumPy. European call only depends on the final price, therefore a single time step is exact, which lets the convergence test reach 10^7 paths. Parameters were: S = 100, K=100, r = 5%(0.05), σ = 20%(0.2), T = 1 year. 

## Convergence Plot

![Convergence plot](convergence_price_paths.png)

The error falls as σ/sqrt(n), where n is the number of paths and σ ≈ 14.7 is the standard deviation of the discounted payoff. Taking 100 times more paths gives 10 times less error. The dots sit slightly below the red line because it shows the standard deviation of the error, while the dots show the average absolute error, which is about 0.8 of that.

## How to run

```
pip install numpy scipy matplotlib
python price_paths.py
```

## Results

At 10^6 paths, Monte Carlo price was 10.4685 +/- 0.0147, against a Black-Scholes price of  10.4506, which falls within 1.2 standard errors, which is expected from sampling noise. Standard deviation of discounted payoff was found to be 14.73. Results may vary as is a random simulation

## Limitations

Only European calls. Kelly sizing planned to do in future as a second class