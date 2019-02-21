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

#################### Exercice 3 ####################

# Create unsharp_masking version
image_gaussian = cv.GaussianBlur(image_original, (201, 201), 0)
image_unsharp_masking = cv.addWeighted(image_original, 1.5, image_gaussian, -0.5, 0)

# Show all versions
cv.imshow('original', image_original)
cv.imshow('gaussian blurring', image_gaussian)
cv.imshow('unsharp masking', image_unsharp_masking)
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
unsharp_masking_output = f'results/unsharp_masking_{args.filename}'
success = cv.imwrite(unsharp_masking_output, image_unsharp_masking)
if not success:
    print(f'Could not write to {unsharp_masking_output}.')