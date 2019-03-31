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
rows, cols = image_original.shape[:2]

#################### Exercice 8 ####################

# Transformation matrix
matrix = np.float32([[1, -0.20, 0], [0, 1, 0]])

# Warp Affine
image_warp_affine = cv.warpAffine(image_original, matrix, (cols, rows))

# Show all versions
cv.imshow('original', image_original)
cv.imshow('warp affine', image_warp_affine)
cv.waitKey(0)
cv.destroyAllWindows()

#################### Save ####################

# Create 'output' folder if not exists
print('Writing output files...')

output_directory = "result/"
if not os.path.isdir(output_directory):
    print('Output folder does not exist, creating it...')
    os.makedirs(output_directory)

# Save
warp_affine_output = f'result/warp_affine_{args.filename}'
success = cv.imwrite(warp_affine_output, image_warp_affine)
if not success:
    print(f'Could not write to {warp_affine_output}.')