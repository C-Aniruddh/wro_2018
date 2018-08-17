import numpy as np
import cv2 as cv
from img2world import undistort
from inverse import perform_inverse
# from actuators.dynamixel.dynamixel_act import DynamixelActuator

import config
import utils.utils
import time


class BlockRecognition:

    def __init__(self, camera_id, optimal_fps):
        self.camera_id = camera_id
        self.fps = optimal_fps
        self.ik = perform_inverse.InverseKinematics()
        # Uncomment the following line when actuating with dynamixels
        # self.dynamixel_act = DynamixelActuator()

    def run(self):

        # Defining some global values
        RED = (0, 0, 255)
        YELLOW = (0, 255, 255)
        BLUE = (255, 0, 0)
        GREEN = (76, 177, 34)
        ORANGE = (39, 127, 255)
        PURPLE = (164, 73, 164)
        VIOLET = (63, 2, 7)

        TRIANGLE = 3
        RECTANGLE = 8
        Z_SHAPE = 8
        L_SHAPE = 6
        T_SHAPE = 2

        # Defining the lower and upper limits for the 3 colors upon calibration
        LOWER_RED1 = np.array([0, 100, 120])
        UPPER_RED1 = np.array([10, 255, 255])
        LOWER_RED2 = np.array([170, 100, 120])
        UPPER_RED2 = np.array([180, 255, 255])
        LOWER_YELLOW = np.array([20, 80, 100])
        UPPER_YELLOW = np.array([40, 255, 255])
        LOWER_BLUE = np.array([91, 100, 100])
        UPPER_BLUE = np.array([111, 255, 255])
        LOWER_ORANGE = np.array([2, 100, 100])
        UPPER_ORANGE = np.array([22, 255, 255])
        LOWER_GREEN = np.array([59, 100, 100])
        UPPER_GREEN = np.array([79, 255, 255])
        LOWER_PURPLE = np.array([140, 100, 100])
        UPPER_PURPLE = np.array([160, 255, 255])
        LOWER_VIOLET = np.array([112, 100, 100])
        UPPER_VIOLET = np.array([132, 255, 255])

        # Setup BlobDetector
        detector = cv.SimpleBlobDetector_create()
        params = cv.SimpleBlobDetector_Params()

        # Filter by Area.
        params.filterByArea = True
        params.minArea = 100
        params.maxArea = 4000

        # Filter by Circularity
        params.filterByCircularity = True
        params.minCircularity = 0.6

        # Filter by Convexity
        params.filterByConvexity = False
        # params.minConvexity = 0.87

        # Filter by Inertia
        params.filterByInertia = True
        params.minInertiaRatio = 0.8

        # Distance Between Blobs
        params.minDistBetweenBlobs = 50

        # Create a detector with the parameters
        detector = cv.SimpleBlobDetector_create(params)

        # Function to draw the result on the lower right corner of an image
        def drawResult(color, shape, img):
            corners = np.array([])
            height, width, _ = img.shape
            text = ""

            if ((shape == RECTANGLE and color == YELLOW) or (shape == RECTANGLE and color == BLUE)):
                corners = np.array([[width - 70, height - 70],
                                    [width - 70, height - 20],
                                    [width - 20, height - 20],
                                    [width - 20, height - 70]])

                if color == YELLOW:
                    text = 'F'
                elif color == BLUE:
                    text = 'A'

            elif ((shape == L_SHAPE and color == ORANGE) or (shape == L_SHAPE and color == VIOLET)):
                corners = np.array([[width - 70, height - 70],
                                    [width - 70, height - 20],
                                    [width - 20, height - 20],
                                    [width - 20, height - 70]])

                if color == ORANGE:
                    text = 'D'
                elif color == VIOLET:
                    text = 'E'

            elif ((shape == Z_SHAPE and color == GREEN) or (shape == Z_SHAPE and color == RED)):
                corners = np.array([[width - 70, height - 70],
                                    [width - 70, height - 20],
                                    [width - 20, height - 20],
                                    [width - 20, height - 70]])

                if color == GREEN:
                    text = 'B'
                elif color == RED:
                    text = 'C'

            elif shape == T_SHAPE and color == PURPLE:
                corners = np.array([[width - 70, height - 70],
                                    [width - 70, height - 20],
                                    [width - 20, height - 20],
                                    [width - 20, height - 70]])

                if color == PURPLE:
                    text = 'G'

            if shape == TRIANGLE or shape == RECTANGLE or shape == L_SHAPE or shape == Z_SHAPE or shape == T_SHAPE:
                # cv.fillPoly(img, [corners], color)
                cv.putText(img, text, (width - 120, height - 24), cv.FONT_HERSHEY_DUPLEX, 2, color, 2, cv.LINE_AA)
            return img

        # Function to find any contour and count its corners
        def getCorners(mask, img):
            _, contours, _ = cv.findContours(mask, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE + 2)
            n = len(contours)
            ret = 0
            for i in range(0, len(contours)):
                cnt = contours[i]
                epsilon = 0.03 * cv.arcLength(cnt, True)
                approx = cv.approxPolyDP(cnt, epsilon, True)
                cv.drawContours(img, [approx], 0, YELLOW, -1)
                for corner in approx:
                    x, y = corner.ravel()
                    cv.circle(img, (x, y), 3, BLUE, -1)
                    # cv.imshow("corners", img)
                ret = max(ret, len(approx))
            return ret, img

        def detect_holes(im):
            overlay = im.copy()

            keypoints = detector.detect(im)
            for k in keypoints:
                # y, x = undistort.picture2world(int(k.pt[0]), int(k.pt[1]))
                x, y = undistort.newpic2world(int(k.pt[0]), int(k.pt[1]))
                # x = round(x)
                # y = round(y)

                """
                Performing inverse kinematics on the coordinate to pick it up.
                Choose any one hole.
                
                ----- OLD ---
                a0, a1, a2, a3, a4, isPossible = self.ik.solve(x, y, config.distance_cam)
                if isPossible:
                    print(a0, a1, a2, a3, a4)
                ---- OLD ----
                
                To calculate inverse kinematic angles and actuate them, create an object for the
                dynamixel actuator (actuators.dynamixel.dynamixel_act)
                
                CODE : [Uncomment when actuating]
                
                da = DynamixelActuator()
                da.actuate(x, y, config.distance_cam)  # to actuate
                
                """


                cv.circle(overlay, (int(k.pt[0]), int(k.pt[1])), int(k.size / 2), (0, 0, 255), -1)
                cv.line(overlay, (int(k.pt[0]) - 20, int(k.pt[1])), (int(k.pt[0]) + 20, int(k.pt[1])), (0, 0, 0), 3)
                cv.line(overlay, (int(k.pt[0]), int(k.pt[1]) - 20), (int(k.pt[0]), int(k.pt[1]) + 20), (0, 0, 0), 3)
                cv.putText(overlay, str("({:.2f}, {:.2f})".format(float(x), float(y))), (int(k.pt[0]), int(k.pt[1])), cv.FONT_HERSHEY_DUPLEX,
                           0.5, (0, 0, 0), 1, cv.LINE_AA)

            opacity = 0.5
            cv.addWeighted(overlay, opacity, im, 1 - opacity, 0, im)
            return im

        # Capturing the video feed

        vid = cv.VideoCapture(self.camera_id)

        while True:
            _, frame = vid.read()

            # Blurring the frame to be ready for color filtering and edge detection
            original = frame
            # frame = cv.undistort(frame, cameraMatrix=config.cameraMatrix, distCoeffs=config.distortionCoeffs, dst=None, newCameraMatrix=None)
            frame = cv.GaussianBlur(frame, (25, 25), 2)
            frame = cv.dilate(frame, np.ones((15, 15), np.uint8))
            frame = cv.erode(frame, np.ones((15, 15), np.uint8))

            # Converting the colors from RGB to HSV
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

            # Generating a binary mask for the 3 colors
            mask_red1 = cv.inRange(hsv, LOWER_RED1, UPPER_RED1)
            mask_red2 = cv.inRange(hsv, LOWER_RED2, UPPER_RED2)
            mask_red = cv.bitwise_or(mask_red1, mask_red2)
            mask_yellow = cv.inRange(hsv, LOWER_YELLOW, UPPER_YELLOW)
            mask_blue = cv.inRange(hsv, LOWER_BLUE, UPPER_BLUE)
            mask_orange = cv.inRange(hsv, LOWER_ORANGE, UPPER_ORANGE)
            mask_green = cv.inRange(hsv, LOWER_GREEN, UPPER_GREEN)
            mask_purple = cv.inRange(hsv, LOWER_PURPLE, UPPER_PURPLE)
            mask_violet = cv.inRange(hsv, LOWER_VIOLET, UPPER_VIOLET)

            # Filtering colors
            red_filter = cv.bitwise_and(frame, frame, mask=mask_red)
            yellow_filter = cv.bitwise_and(frame, frame, mask=mask_yellow)
            blue_filter = cv.bitwise_and(frame, frame, mask=mask_blue)
            orange_filter = cv.bitwise_and(frame, frame, mask=mask_orange)
            green_filter = cv.bitwise_and(frame, frame, mask=mask_green)
            purple_filter = cv.bitwise_and(frame, frame, mask=mask_purple)
            violet_filter = cv.bitwise_and(frame, frame, mask=mask_violet)

            # Defining contours and count the corners of each contour
            red_corners, red_contours = getCorners(mask_red, red_filter.copy())
            yellow_corners, yellow_contours = getCorners(mask_yellow, yellow_filter.copy())
            blue_corners, blue_contours = getCorners(mask_blue, blue_filter.copy())
            orange_corners, orange_contours = getCorners(mask_orange, orange_filter.copy())
            green_corners, green_contours = getCorners(mask_green, green_filter.copy())
            purple_corners, purple_contours = getCorners(mask_purple, purple_filter.copy())
            violet_corners, violet_contours = getCorners(mask_violet, violet_filter.copy())

            # Printing the number of corners in each color contour for debugging
            # ryb = str(red_corners) + ' ' + str(yellow_corners) + ' ' + str(blue_corners)
            # print(ryb)
            print("R = {}, Y = {}, B = {}, O = {}, G = {}, P = {}, V = {}".format(red_corners, yellow_corners,
                                                                                  blue_corners, orange_corners,
                                                                                  green_corners, purple_corners,
                                                                                  violet_corners))

            # Drawing the result on the original image
            if red_corners >= 5:
                original = drawResult(RED, red_corners, original.copy())
                original = detect_holes(original)
            if yellow_corners >= 3:
                original = drawResult(YELLOW, yellow_corners, original.copy())
                original = detect_holes(original)
            if blue_corners >= 3:
                original = drawResult(BLUE, blue_corners, original.copy())
                original = detect_holes(original)
            if green_corners >= 5:
                original = drawResult(GREEN, green_corners, original.copy())
                original = detect_holes(original)
            if orange_corners >= 4:
                original = drawResult(ORANGE, orange_corners, original.copy())
                original = detect_holes(original)
            if purple_corners >= 5:
                original = drawResult(PURPLE, purple_corners, original.copy())
                original = detect_holes(original)
            if violet_corners >= 5:
                original = drawResult(VIOLET, violet_corners, original.copy())
                original = detect_holes(original)

            cv.imshow('Original', original)

            if cv.waitKey(1) & 0xff == ord('q'):
                break

        vid.release()
        cv.destroyAllWindows()
