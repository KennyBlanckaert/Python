import argparse
import os
import sys

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

#################### Preparation ####################

# Parsing variables
parser = argparse.ArgumentParser()
parser.add_argument(
    'filename',
    help='Image filename used for conversion and saving.',
    type=str
)
args = parser.parse_args()

# Save image path in variable
image_name = f'images/{args.filename}'

# Check if given path exists
if not os.path.exists(image_name):
    print('Image does not exist.')
    sys.exit(1)

# Read RGB image
image_original = cv.imread(image_name, cv.IMREAD_COLOR)

#################### Exercice 5 ####################

# Create grayscale version
image_gray = cv.cvtColor(image_original, cv.COLOR_BGR2GRAY)

sobely = cv.Sobel(image_gray, cv.CV_64F, 0, 1, 5)
sobelx = cv.Sobel(image_gray, cv.CV_64F, 1, 0, 5)

# Print Sobel result
print("Sobel Y")
print(sobely), print()
print("Sobel X:")
print(sobelx), print()

# Put everything togheter in a plot
plt.subplot(2,1,1)
plt.imshow(image_gray, cmap = 'gray')
plt.title('Original')
plt.xticks([]), plt.yticks([])

plt.subplot(2,2,3)
plt.imshow(sobelx, cmap = 'gray')
plt.title('Sobel X'),
plt.xticks([]), plt.yticks([])

plt.subplot(2,2,4)
plt.imshow(sobely, cmap = 'gray')
plt.title('Sobel Y')
plt.xticks([]), plt.yticks([])

plt.show()
