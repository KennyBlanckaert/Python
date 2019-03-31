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

#################### Exercice 10 ####################

# step 1
gaussian_1D = cv.getGaussianKernel(9, 1)

# step 2
matrix_2D = np.ones((9, 9))
matrix_2D[:,4] = gaussian_1D[:,0]

# step 3
kernel_1D_lower_deviation = cv.getGaussianKernel(9, 0)
kernel_1D_lower_deviation = np.transpose(kernel_1D_lower_deviation)

# step 4
gaussian_2D = cv.filter2D(matrix_2D, -1, kernel_1D_lower_deviation)

# step 5
filter_DoG = cv.Sobel(gaussian_2D, cv.CV_64F, 0, 1, 9)
#filter_DoG = cv.Sobel(gaussian_2D, cv.CV_64F, 1, 0, 9)

# step 6
rotation_matrix = cv.getRotationMatrix2D((4, 4), 75, 1)

# step 7
rotated_filter_DoG = cv.warpAffine(filter_DoG, rotation_matrix, (9, 9))

# step 8
image_grayscale = cv.cvtColor(image_original, cv.COLOR_BGR2GRAY)

# step 9
image_edges = cv.filter2D(image_grayscale, -1, rotated_filter_DoG)
image_edges = np.absolute(image_edges)

# show
cv.imshow("result", image_edges)
cv.waitKey(0)
cv.destroyAllWindows()

#################### Save ####################

# Create 'result' folder if not exists
print('Writing output files...')

output_directory = "result/"
if not os.path.isdir(output_directory):
    print('Output folder does not exist, creating it...')
    os.makedirs(output_directory)

# Save
edge_detection_output = f'result/custom_edge_detection_{args.filename}'
success = cv.imwrite(edge_detection_output, image_edges)
if not success:
    print(f'Could not write to {edge_detection_output}.')