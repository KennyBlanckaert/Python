import matplotlib.pyplot as plt

# Information
labels = ('Python', 'Java', 'Javascript', 'C#', 'PHP', 'C/C++', 'R', 'Objective-C', 'Swift', 'Matlab')
percentages = [25.36, 21.56, 8.4, 7.63, 7.31, 6.4, 4.01, 3.21, 2.69, 2.06]
explode = (0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0) 

# Receice plot
fig1, ax1 = plt.subplots()

# Change plot
ax1.pie(percentages, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)

plt.show()