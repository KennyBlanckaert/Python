import argparse
import os
import sys

import cv2 as cv
import numpy as np

from matplotlib import pyplot as plt

#################### Functions ######################

def create_DoGfilter(scale, orientation):

    gaussian_1D = cv.getGaussianKernel(scale, 1)

    middle = int(np.floor(scale / 2))
    matrix_2D = np.ones((scale, scale))
    matrix_2D[:, middle] = gaussian_1D[:, 0]

    kernel_1D_lower_deviation = cv.getGaussianKernel(scale, 0)
    kernel_1D_lower_deviation = np.transpose(kernel_1D_lower_deviation)

    gaussian_2D = cv.filter2D(matrix_2D, -1, kernel_1D_lower_deviation)

    #filter_DoG = cv.Sobel(gaussian_2D, cv.CV_64F, 0, 1, scale)
    filter_DoG = cv.Sobel(gaussian_2D, cv.CV_64F, 1, 0, scale)

    rotation_matrix = cv.getRotationMatrix2D((middle, middle), orientation, 1)

    rotated_filter_DoG = cv.warpAffine(filter_DoG, rotation_matrix, (scale, scale))

    return rotated_filter_DoG


#################### Preparation ####################

# Parsing variables
parser = argparse.ArgumentParser()
parser.add_argument(
    'filename',
    help='Image filename used for conversion and saving.',
    type=str
)
parser.add_argument(
    'mask',
    help='Mask filename used for plotting.',
    type=str
)

args = parser.parse_args()

# Save image path in variable
image_path = f'images/{args.filename}'
mask_path = f'images/{args.mask}'

# Check if given path exists
if not os.path.exists(image_path):
    print('Image does not exist.')
    sys.exit(1)
if not os.path.exists(mask_path):
    print('Mask does not exist.')
    sys.exit(1)

# Read RGB image
image_original = cv.imread(image_path, cv.IMREAD_COLOR)
image_grayscale = cv.cvtColor(image_original, cv.COLOR_BGR2GRAY)
rows, cols = image_original.shape[:2]
blocks = (int(rows / 16), int(cols / 16))

mask = cv.imread(mask_path, cv.IMREAD_GRAYSCALE)

#################### Exercice 14 ####################

scales = [5, 20]
orientations = [15, 30, 60, 90, 25, 70]

# Per-block processing
road_blocks = []
non_road_blocks = []

### Foreach filter
for scale in scales:
    for orientation in orientations:

        ### Filter image
        filter_DoG = create_DoGfilter(scale, orientation)
        result = cv.filter2D(image_grayscale, -1, filter_DoG)
        result = np.absolute(result)

        ### Average variables
        white_count = 0
        black_count = 0
        white_sum = 0
        black_sum = 0

        ### Foreach block
        for x in range(0, blocks[0]):
            for y in range(0, blocks[1]):

                ### Max in block
                crop = result[x * 16 : (x+1) * 16, y * 16 : (y+1) * 16] 
                maximum = np.max(crop)

                ### Determine part of mask
                if (mask[int(x*16)][int(y*16)] == 255):
                    white_count += 1
                    white_sum += maximum
                else:
                    black_count += 1
                    black_sum += maximum
                
        ### Harvest allblock results
        road_blocks.append(int(white_sum / white_count))
        non_road_blocks.append(int(black_sum / black_count))


plt.plot(road_blocks)
plt.plot(non_road_blocks)
plt.show()
