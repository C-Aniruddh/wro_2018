import config
import numpy as np
from numpy.linalg import inv

cameraMatrix = config.cameraMatrix
distortionCoeffs = config.distortionCoeffs
rvct = config.rvct
tvct = config.tvct
distance_cam = config.distance_cam


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def world_coordinates(u, v):
    world_coord = np.array([[u], [v], [1]])
    world_coord = inv(cameraMatrix) * world_coord
    world_coord = world_coord * distance_cam
    world_x = world_coord[0][0]
    world_y = world_coord[1][1]
    """print(world_x, world_y)"""
    return world_x, world_y
