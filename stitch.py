# import the necessary packages
from panorama import Stitcher
import cv2

#Enter the paths to the two images
pathA = "hill1.jpg"
pathB = "hill2.jpg"

# stitch the images together to create a panorama
pano = Stitcher()
imageA = pano.loadAndResize(pathA)
imageB = pano.loadAndResize(pathB)


result,vis= pano.stitch([imageA, imageB],"SIFT", showMatches = True)

# show the images
cv2.imshow("Image A", imageA)
cv2.imshow("Image B", imageB)
cv2.imshow("Keypoint Matches", vis)
cv2.imshow("Result", result)
cv2.waitKey(0)