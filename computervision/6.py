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

# Create kernel
kernel = np.zeros((15, 15), int)
np.fill_diagonal(kernel, [1,1,1,1,1,1,1,0,0,0,0,0,0,0,0])
print(kernel)
print()

# Create filter2D version
image_filter2D = cv.filter2D(image_original, -1, 1/7*kernel)

# Show all versions
cv.imshow('original', image_original)
cv.imshow('filter2D', image_filter2D)
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
filter2D_output = f'results/filter2D_{args.filename}'
success = cv.imwrite(filter2D_output, image_filter2D)
if not success:
    print(f'Could not write to {filter2D_output}.')