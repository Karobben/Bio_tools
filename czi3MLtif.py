#!/usr/bin/env python3
import numpy as np
from aicspylibczi import CziFile
import tifffile

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i','-I','--input')

args = parser.parse_args()
File = args.input


czi = CziFile(File)
image = czi.read_image()[0][0][0]
tifffile.imwrite(File + '.tif', image)
