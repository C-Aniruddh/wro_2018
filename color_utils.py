import numpy as np
import cv2 as cv

LOWER_RED1 = np.array([0, 100, 120])
UPPER_RED1 = np.array([10, 255, 255])
LOWER_RED2 = np.array([170, 100, 120])
UPPER_RED2 = np.array([180, 255, 255])
LOWER_YELLOW = np.array([20, 100, 100])
UPPER_YELLOW = np.array([40, 255, 255])
LOWER_BLUE = np.array([89, 100, 100])
UPPER_BLUE = np.array([109, 255, 255])
LOWER_ORANGE = np.array([6, 100, 100])
UPPER_ORANGE = np.array([26, 255, 255])
LOWER_GREEN = np.array([31, 100, 100])
UPPER_GREEN = np.array([51, 255, 255])
LOWER_PURPLE = np.array([140, 100, 100])
UPPER_PURPLE = np.array([160, 255, 255])
LOWER_VIOLET = np.array([101, 100, 100])
UPPER_VIOLET = np.array([121, 255, 255])

def getCorners(mask, img):
    _, contours, _ = cv.findContours(mask, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE + 2)
    n = len(contours)
    ret = 0
    for i in range(0, len(contours)):
        cnt = contours[i]
        epsilon = 0.03 * cv.arcLength(cnt, True)
        approx = cv.approxPolyDP(cnt, epsilon, True)
        for corner in approx:
            x, y = corner.ravel()
        ret = max(ret, len(approx))
    return ret, img


def get_color(frame):
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

    list_corners = [red_corners, yellow_corners, blue_corners, orange_corners, green_corners, purple_corners, violet_corners]
    ind = get_max(list_corners)
    shape = get_shape(ind)

    return shape


def get_max(in_list):
    max_data = max(in_list)
    max_index = in_list.index(max_data)
    return max_index


def get_shape(index):
    shape = ""
    if index == 0:
        shape = "S"
    elif index == 1:
        shape = "O"
    elif index == 2:
        shape = "I"
    elif index == 3:
        shape = "L"
    elif index == 4:
        shape = "Z"
    elif index == 5:
        shape = "T"
    elif index == 6:
        shape = "J"
    return shape
