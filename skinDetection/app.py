import sys  # for Command Line Arguments
from skindetector import SkinDetector
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-f', "--filename", help="Enter the file name with path", required=True)
args = vars(ap.parse_args())

imageName = args["filename"]

detector = SkinDetector(imageName)
detector.find_skin()