import argparse
import cv2
import os
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
ap.add_argument("-p1", "--param1", required = True, help = "threshold for edge detection")
ap.add_argument("-p2", "--param2", required = True, help = "accumulator threshold for the circle centers")
ap.add_argument("-minR", "--minRadius", required = True, help = "minimum radius (in pixels) for detected circles")
ap.add_argument("-maxR", "--maxRadius", required = True, help = "maximum radius (in pixels) for detected circles")
ap.add_argument("-f", "--fuzzy", required = True, help = "length in pixels of precipitate region (mag dependent)")

args = vars(ap.parse_args())

# load the image, clone it for output display, and then convert it to grayscale
image = cv2.imread(args["image"])
output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#gaussian blur is necessary to get rid of high frequency, noisy components in image

inter = cv2.GaussianBlur(gray, (3, 3), cv2.BORDER_DEFAULT);

# detect circles in the image

circles = cv2.HoughCircles(inter, cv2.HOUGH_GRADIENT,1.2,200,len(gray)/4,param1=int(args["param1"]),param2=int(args["param2"]),minRadius=int(args["minRadius"]),maxRadius=int(args["maxRadius"]))

#save hyperparameters ie: save as .csv  can save as csv in order for reproducibility darkfield vs brightfield

ls = []
fuz = int(args["fuzzy"])

# ensure at least some circles were found
if circles is not None:
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		"""
        draw the circle in the output image, then draw a rectangle corresponding to the center of the circle.
        circle is cropped, sobel filtered, and histogram of the sobel filtered ROI is saved.
		"""
		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

		canvas = np.zeros(image.shape[:2], np.uint8) #param for circles drawn on output image
		color = (255, 255, 255) #param for circles drawn on output image
		thickness = -1 #param for circles drawn on output image
		cv2.circle(canvas, (x, y), (r + fuz), color, thickness) #param for circles drawn on output image

		imageCopy = image.copy() #prep to crop roi where circle
		imageCopy[canvas == 0] = (0, 0, 0)
		roi = imageCopy[y - (r + fuz): y + (r + fuz), x - (r + fuz): x + (r + fuz)]
		roi.astype(np.uint8)

		inner_r = r #param for cropping
		outer_r = int(roi.shape[:2][1] / 2) #param for cropping
		mask1 = np.zeros_like(roi) #param for cropping
		mask2 = np.zeros_like(roi) #param for cropping
		mask1 = cv2.circle(mask1, (round(outer_r), round(outer_r)), inner_r, (255, 255, 255), -1) #crop
		mask2 = cv2.circle(mask2, (round(outer_r), round(outer_r)), outer_r, (255, 255, 255), -1) #crop
		mask = cv2.subtract(mask2, mask1)
		roi2 = cv2.bitwise_and(roi, mask) #cropped region
		#take nonzero values of roi2 and average to find pixel value
		avg_pix = np.mean(np.nonzero(roi2))

		canvas2 = np.zeros(image.shape[:2], np.uint8) #prepping to find avg pixel value  on cropped image
		cv2.circle(canvas, (x, y), (r + fuz), color, thickness)
		imageCopy2 = image.copy()
		imageCopy2[canvas == 0] = avg_pix #to make sure that the sobel filter doesn't think that the boundary between the image and the mask is a derivative
        # #to be sure, you should threshold the histogram that this script returns!
		roi3 = imageCopy2[y - (r + fuz): y + (r + fuz), x - (r + fuz): x + (r + fuz)]
		cv2.imshow("output", np.hstack([roi3]))
		cv2.waitKey(0)
		ls.append(avg_pix) #again, avg_pix isn't very useful, but at least ls keeps track of how many circles there are

		sobel_horizontal_b = cv2.Sobel(roi, cv2.CV_64F, 1, 0, ksize=1) #now for the actual filter step
		sobel_vertical_b = cv2.Sobel(roi, cv2.CV_64F, 0, 1, ksize=1)

		abs_grad_x_b = cv2.convertScaleAbs(sobel_horizontal_b)
		abs_grad_y_b = cv2.convertScaleAbs(sobel_vertical_b)

		grad_b = cv2.addWeighted(abs_grad_x_b, 0.5, abs_grad_y_b, 0.5, 0)
		#save grad_b as a histogram so you can plot it!
		hist_b = cv2.calcHist([grad_b], [0], None, [256], [0, 256])
		np.savetxt(f'{os.path.dirname(args["image"])}/{os.path.basename(args["image"])[0:-4]}_bead_hist_{len(ls)}.csv', hist_b, delimiter=",")
		# p = cv2.bitwise_and(roi, roi, mask=mask)
		cv2.imshow("output", np.hstack([grad_b]))
		cv2.waitKey(0)

	cv2.imshow("output", np.hstack([image, output])) # show the output image
	cv2.waitKey(0)