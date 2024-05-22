# import the necessary packages
import numpy as np
import imutils
import cv2

class Stitcher:
      
	def __init__(self):
		return
	
	def loadAndResize(self,path):
		image = cv2.imread(path)
		image = imutils.resize(image, width=400)
		return image
	
	def convertToGrayscale(self,image):
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		return gray
	
	def detectFeatures(self,image, detector = "ORB"):
		if detector == "ORB":
			descriptor = cv2.ORB_create()
		elif detector == "SIFT":
			descriptor = cv2.SIFT_create()

		(kps, features) = descriptor.detectAndCompute(image, None)
		
        # showing the images with their key points finded by the detector
		key_image = cv2.drawKeypoints(image,kps,None)
		cv2.imshow("Keypoints of Image: ",key_image)
		cv2.waitKey()

        #Print list of descriptors and their shape       
		print(f'Descriptors of Image {features}')
		print('------------------------------')
		print(f'Shape of descriptor of image {features.shape}')

		# return a tuple of keypoints and features
		return (kps, features)
	
	def matchFeatures(self, feature1, feature2, detector = "ORB"):
		if detector == "ORB":
			matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
			raw_matches = matcher.match(feature1,feature2)
			matches = sorted(raw_matches, key=lambda x: x.distance)
		elif detector =="SIFT":
			matcher = cv2.BFMatcher()
			raw_matches = matcher.knnMatch(feature1,feature2,k=2)
			ratio = 0.75 #Lowe's ratio
			matches = []
			for m, n in raw_matches:
				if m.distance < ratio * n.distance:
					matches.append(m)
		return matches
	
	def estimate_homography(self,kps1, kps2, matches, threshold=5):
		# construct the two sets of points
	    # compute the homography between the two sets of points
		src_pts = np.float32([kps1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
		dst_pts = np.float32([kps2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
		H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, threshold)
		
		return H
	
	def warp_images(self,img1, img2, H):
		warped_img = cv2.warpPerspective(img1, H,(img1.shape[1]+img2.shape[1], img1.shape[0]))
		warped_img[0:img2.shape[0], 0:img2.shape[1]] = img2
		
		return warped_img
	
	def stitch(self,images,detector = "ORB", showMatches = False):
	    # unpack the images, then detect keypoints and extract
		# local invariant descriptors from them
		(image2, image1) = images
		gray1 = self.convertToGrayscale(image1)
		gray2 = self.convertToGrayscale(image2)
		(kps1, features1) = self.detectFeatures(gray1, detector)
		(kps2, features2) = self.detectFeatures(gray2, detector)
		# match features between the two images
		M = self.matchFeatures(features1, features2, detector)
		
		# if the match is None, then there aren't enough matched keypoints to create a panorama
		if M is None:
			return None
		# otherwise, estimate homography and apply a perspective warp to stitch the images together
		
		H = self.estimate_homography(kps1, kps2, M)
		result = self.warp_images(image1, image2, H)
	
		# check to see if the keypoint matches should be visualized
		if showMatches:
			if detector == "ORB":
				vis = cv2.drawMatches(image1,kps1,image2,kps2,M,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
			elif detector =="SIFT":
				vis = cv2.drawMatchesKnn(image1, kps1, image2, kps2, [M], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
			# return a tuple of the stitched image and the visualization
			return (result, vis)
		# return the stitched image
		return result
		
	

		
		
		
    

