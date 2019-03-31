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

#################### Exercice 11 ####################

image_grayscale = cv.cvtColor(image_original, cv.COLOR_BGR2GRAY)
image_edges = cv.Canny(image_grayscale, 50, 150, apertureSize = 5)

lines = cv.HoughLines(image_edges, 1, np.pi / 180, 100)
for x in range(0, len(lines)):
    for rho, theta in lines[x]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
        pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))

        cv.line(image_original, pt1, pt2, (0, 0, 0), 2)

# show
cv.imshow("Canny", image_edges)
cv.imshow("Hough", image_original)
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
canny_output = f'result/canny_edge_detection_{args.filename}'
hough_output = f'result/hough_line_detection_{args.filename}'
success_1 = cv.imwrite(canny_output, image_edges)
success_2 = cv.imwrite(hough_output, image_original)
if not success_1:
    print(f'Could not write to {canny_output}.')
if not success_2:
    print(f'Could not write to {hough_output}.')