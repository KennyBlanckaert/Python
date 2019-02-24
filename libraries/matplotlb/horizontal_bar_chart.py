import matplotlib.pyplot as plt
import numpy as np

# Information
labels = ('Python', 'Java', 'Javascript', 'C#', 'PHP')
y_pos = np.arange(len(labels))
percentages = [25.36, 21.56, 8.4, 7.63, 7.31]

# Receive plot
fig, ax = plt.subplots()

# Add information
ax.barh(y_pos, percentages, align='center', color='purple')

# y-axis
ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.invert_yaxis() 

# Title
ax.set_title('Programming languages')

# x-axis
ax.set_xlabel('Usability')

# Show
plt.show()