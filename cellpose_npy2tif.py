#!/usr/bin/env python3
import numpy as np
import tifffile

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i','-I','--input')

args = parser.parse_args()
File = args.input

A = np.load(File,allow_pickle=True).all()

image = A['masks']
np.save(File+ "_mask.npy", image)
