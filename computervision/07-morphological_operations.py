import argparse
import os
import sys

import cv2 as cv
import numpy as np

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

#################### Exercice 6 ####################

# Kernels
square_kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
elliptic_kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
cross_kernel = cv.getStructuringElement(cv.MORPH_CROSS, (5, 5))
kernel = square_kernel

# Erosion
image_erosion = cv.erode(image_original, kernel)

# Dilation
image_dilation = cv.dilate(image_original, kernel)

# Opening - Closing - Gradient
image_opening = cv.morphologyEx(image_original, cv.MORPH_OPEN, kernel)
image_closing = cv.morphologyEx(image_original, cv.MORPH_CLOSE, kernel)
image_gradient = cv.morphologyEx(image_original, cv.MORPH_GRADIENT, kernel)

# Show all versions
cv.imshow('original', image_original)
cv.imshow('erosion', image_erosion)
cv.imshow('dilation', image_dilation)
cv.imshow('opening', image_opening)
cv.imshow('closing', image_closing)
cv.imshow('gradient', image_gradient)
cv.waitKey(0)
cv.destroyAllWindows()

#################### Save ####################

# Create 'output' folder if not exists
print('Writing output files...')

output_directory = "results/"
if not os.path.isdir(output_directory):
    print('Output folder does not exist, creating it...')
    os.makedirs(output_directory)

# Save
cv.imwrite(f'results/erosion_{args.filename}', image_erosion)
cv.imwrite(f'results/dilation_{args.filename}', image_dilation)
cv.imwrite(f'results/opening_{args.filename}', image_opening)
cv.imwrite(f'results/closing_{args.filename}', image_closing)
cv.imwrite(f'results/gradient_{args.filename}', image_gradient)
