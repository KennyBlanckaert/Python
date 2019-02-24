import matplotlib.pyplot as plt
import math
import numpy as np

# x**2
plt.plot([x**2 for x in range(-10, 11)])
plt.show()

# x**3
plt.plot([x**3 for x in range(-10, 11)])
plt.show()

# Sin x (2 * PI * frequency * time_range * x)
frequency = 3
t = 1000
x = np.arange(t)
y = np.sin(2 * np.pi * frequency * x / t)
plt.plot(x, y)
plt.xlabel('sample(n)')
plt.ylabel('voltage(V)')
plt.show()