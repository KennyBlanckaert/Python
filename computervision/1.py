import argparse
import os
import sys

import cv2 as cv
import numpy as np

# Parsing variables
parser = argparse.ArgumentParser()
parser.add_argument(
    'filename',
    help='Image filename used for conversion and saving.',
    type=str
)
args = parser.parse_args()

# Save image path in variable
# Using f'...' to use variables
image_name = f'images/{args.filename}'

# Check if given path exists
if not os.path.exists(image_name):
    print('Image does not exist.')
    sys.exit(1)

# Read RBG image
image_color = cv.imread(image_name, cv.IMREAD_COLOR)
cv.imshow('color', image_color)
cv.waitKey(0)
cv.destroyAllWindows()

# Convert to grayscale
image_gray = cv.cvtColor(image_color, cv.COLOR_BGR2GRAY)
cv.imshow('grayscale', image_gray)
cv.waitKey(0)
cv.destroyAllWindows()

# Thresholding
ret, image_threshold = cv.threshold(image_gray, 127, 255, cv.THRESH_BINARY)
cv.imshow('threshold', image_threshold)
cv.waitKey(0)
cv.destroyAllWindows()

# Create 'output' folder if not exists
print('Writing output files...')

output_directory = "results/"
if not os.path.isdir(output_directory):
    print('Output folder does not exist, creating it...')
    os.makedirs(output_directory)

# Save
grayscale_output = f'results/grayscale_{args.filename}'
success = cv.imwrite(grayscale_output, image_gray)
if not success:
    print(f'Could not write to {grayscale_output}.')

threshold_output = f'results/threshold_{args.filename}'
success = cv.imwrite(threshold_output, image_threshold)
if not success:
    print(f'Could not write to {threshold_output}.')