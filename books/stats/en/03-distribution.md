# 3. Random variables and distributions

## What you will learn

- Random variables, and the difference between discrete and continuous
- Probability mass functions, probability density functions and distribution functions
- Joint, marginal and conditional distributions
- Statistical independence

## Random variables

Something like the number on a die — a value is decided each time you try, and how likely each value is (its probability) is fixed — is called a **random variable**. We write it with a capital letter $X$, and the value that actually came out with a small letter $x$.

| Type | Values | Examples | How probability is expressed |
| --- | --- | --- | --- |
| Discrete | Separate values | The number on a die, visitors per day | Probability mass function $P(X = x)$ |
| Continuous | Any value in a range | Height, temperature, a cow's weight | Probability density function $f(x)$ |

For a continuous random variable, the probability of getting exactly one value is 0. We think of probability over a range, as an area under the density function.

$$P(a \le X \le b) = \int_a^b f(x)\,dx$$

## Distribution function

The "probability of being $x$ or less" is called the **distribution function** (cumulative distribution function).

$$F(x) = P(X \le x)$$

- As $x$ gets larger, it increases (it never decreases), taking values from 0 to 1
- For a continuous variable, differentiating $F(x)$ gives the density function $f(x)$
- $P(a < X \le b) = F(b) - F(a)$

## Standard normal distribution

The normal distribution with mean 0 and variance 1 is called the **standard normal distribution** $N(0, 1)$. Its density function has this bell shape.

$$\phi(z) = \frac{1}{\sqrt{2\pi}}\, e^{-z^2/2}$$

Its distribution function is written $\Phi(z)$. A commonly used value is $\Phi(1.96) \approx 0.975$, so 95% falls within $-1.96 \le Z \le 1.96$ (Chapter 5).

## Joint and marginal distributions

How likely each pair of values of two random variables $X, Y$ is, is called the **joint distribution**. Here is an example with the weather $X$ and whether you carry an umbrella $Y$.

| | Umbrella | No umbrella | Total (marginal distribution of $X$) |
| --- | --- | --- | --- |
| Sunny | 0.1 | 0.5 | 0.6 |
| Rainy | 0.3 | 0.1 | 0.4 |
| Total (marginal distribution of $Y$) | 0.4 | 0.6 | 1.0 |

The distribution of just one of them is called the **marginal distribution**, and you get it by adding over the other variable.

$$P(X = x) = \sum_{y} P(X = x, Y = y)$$

## Conditional distribution

"The distribution of $Y$ once you know that $X = x$" is called the **conditional distribution**.

$$P(Y = y \mid X = x) = \frac{P(X = x, Y = y)}{P(X = x)}$$

- Probability of carrying an umbrella on a rainy day: $0.3 / 0.4 = 0.75$
- Probability of carrying an umbrella on a sunny day: $0.1 / 0.6 \approx 0.17$

## Statistical independence

When the joint probability equals the product of the marginal probabilities for every pair, $X$ and $Y$ are **independent**.

$$P(X = x, Y = y) = P(X = x)\,P(Y = y)$$

If they are independent, knowing $X$ does not change the distribution of $Y$ ($P(Y \mid X) = P(Y)$).
In the example above, $P(\text{rain}, \text{umbrella}) = 0.3$, but $P(\text{rain})P(\text{umbrella}) = 0.4 \times 0.4 = 0.16$, so they are not independent (whether you carry an umbrella depends on the weather).

## Summary

- Random variables are discrete (probability mass function) or continuous (probability density function; probability is an area)
- The distribution function $F(x)=P(X\le x)$ increases from 0 to 1
- Adding up the joint distribution gives the marginal distribution; dividing a joint probability by a marginal probability gives the conditional distribution
- When the joint probability is always the product of the marginal probabilities, the variables are independent
