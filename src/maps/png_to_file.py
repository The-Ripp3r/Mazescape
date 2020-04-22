import argparse
import numpy as np
from PIL import Image

"""
Takes in png representation of map and converts it to the
appropriate text file format
"""

# Read in arguments
parser = argparse.ArgumentParser(description="Parser")
parser.add_argument("--png_path", type=str, required=True)
parser.add_argument("--out_file", type=str, default='out.txt')
parser.add_argument("--threshold", type=int, default=127)
parser.add_argument("--width", type=int, default=80)
parser.add_argument("--height", type=int, default=60)
parser.add_argument("--white_becomes", type=str, default='1')
parser.add_argument("--black_becomes", type=str, default='.')
args = parser.parse_args()

# Read in image
img = Image.open(args.png_path, 'r')
img = img.resize((args.width, args.height))
img = img.convert('L')

# Threshold image
img = img.point(lambda p: p > args.threshold)

# Put in correct format
arr = np.asarray(img.getdata()).reshape(
        img.size[1], img.size[0])
str_arr = arr.astype(str)
str_arr[arr == 0] = args.black_becomes
str_arr[arr == 1] = args.white_becomes

# Write to file
np.savetxt(args.out_file, str_arr, fmt='%s', delimiter='')
