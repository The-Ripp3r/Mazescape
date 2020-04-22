import argparse
import numpy as np
from PIL import Image

"""
Reads in text file in our specified format and returns a
png file where the walls are black and the path is white
"""

# Read in arguments
parser = argparse.ArgumentParser(description="Parser")
parser.add_argument("--txt_path", type=str, required=True)
parser.add_argument("--out_file", type=str, default="out.png")
parser.add_argument("--scale", type=float, default=1.0)
args = parser.parse_args()

# Convert to image
rows_list = np.genfromtxt(args.txt_path, dtype=str, delimiter="")
arr = []
replace_list = [("1", "0"), ("G", "1"), ("P", "1"), (".", "1")]
for row in rows_list:
    for old, new in replace_list:
        row = row.replace(old, new)
    arr.append(list(row))

arr = np.array(arr)
arr = arr.astype(int)
print(arr.shape)
rescaled = (255.0 / arr.max() * (arr - arr.min())).astype(np.uint8)
im = Image.fromarray(rescaled)
im = im.resize(((int)(im.size[0] * args.scale), (int)(im.size[1] * args.scale)))
im.save(args.out_file)
