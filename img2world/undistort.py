import cv2
import numpy as np
from numpy.linalg import inv
import utils.utils
import config

cameraMatrix = config.cameraMatrix
distortionCoeffs = config.distortionCoeffs
rvct = config.rvct
tvct = config.tvct
distance_cam = config.distance_cam


def undistort(src, cameraMatrix, distortionCoeffs):
    fx, fy, cx, cy = cameraMatrix[0, 0], cameraMatrix[1, 1], cameraMatrix[0, 2], cameraMatrix[1, 2]
    k1, k2, p1, p2, k3 = distortionCoeffs

    def _map(u, v):
        x1 = (u - cx) / fx
        y1 = (v - cy) / fy
        r2 = x1 ** 2 + y1 ** 2
        k = 1 + k1 * r2 + k2 * r2 ** 2 + k3 * r2 ** 3
        x2 = k * x1 + 2 * p1 * x1 * y1 + p2 * (r2 + 2 * x1 ** 2)
        y2 = k * y1 + p1 * (r2 + 2 * y1 ** 2) + 2 * p2 * x1 * y1
        u1 = x2 * fx + cx
        u2 = y2 * fx + cy
        return u1, u2

    shape = src.shape
    mapxy = np.array([[_map(i, j) for i in range(shape[1])] for j in range(shape[0])], dtype=np.float32)
    dst = cv2.remap(src, mapxy, None, cv2.INTER_LINEAR)
    return dst


def _testUndistort():
    src = cv2.imread('Data/transform/3.jpg')
    dst = cv2.undistort(src, cameraMatrix, distortionCoeffs)
    dst2 = undistort(src, cameraMatrix, distortionCoeffs)
    utils.utils.showimg(src, dst, dst2)


def _testProjectPoints():
    camera = cv2.VideoCapture(1)
    ret, src = camera.read()
    line = input("input object point x y: ")
    while line:
        x, y = [int(v) for v in line.split()]
        pnt, jac = cv2.projectPoints(np.array([[x, y, 0]], dtype=np.float32),
                                     rvct, tvct, cameraMatrix, distortionCoeffs)
        print(pnt, jac, sep='\n')
        img = src.copy()
        print(pnt[0][0])
        utils.utils.markpos(img, pnt[0][0])
        utils.utils.showimg(img)
        line = input("input object point x y: ")


def _pic2cam(u, v):
    '''convert from picture coordinate to camera coordinate'''
    fx, fy, cx, cy = cameraMatrix[0, 0], cameraMatrix[1, 1], cameraMatrix[0, 2], cameraMatrix[1, 2]
    k1, k2, p1, p2, k3 = distortionCoeffs
    x, y = (u - cx) / fx, (v - cy) / fy

    # distrot equation
    def Distort(var):
        '''Distrot and Jacobian'''
        x, y = var[0, 0], var[1, 0]
        r2 = x ** 2 + y ** 2
        r4 = r2 ** 2
        r6 = r2 ** 3
        K = k3 * r6 + k2 * r4 + k1 * r2 + 1
        DK = (6 * k3 * r4 + 4 * k2 * r2 + 2 * k1)
        DP1, DP2 = 2 * (x * p2 + y * p1), 2 * (x * p1 + y * p2)
        return (np.matrix([[K * x + 2 * p1 * x * y + p2 * (r2 + 2 * x * x)],
                           [K * y + p1 * (r2 + 2 * y * y) + 2 * p2 * x * y]]),
                np.matrix([[K + DK * x * x + DP1 + 2 * p2, DK * x * y + DP2],
                           [DK * x * y + DP2, K + DK * y * y + DP1 + 2 * p1]]))

    # find (x0, y0) that Distrot(x0, y0) = (x, y): Newton method
    dst = np.matrix([[x], [y]])
    var = np.matrix([[x], [y]])
    for i in range(10):
        cur, J = Distort(var)
        delta = dst - cur
        if (abs(delta) < 0.0001).all(): break
        var = var + J.I * delta
    # print(i)
    return var[0, 0], var[1, 0]


def picture2world(u, v):
    x, y = _pic2cam(u, v)
    RT = cv2.Rodrigues(rvct)[0].transpose().view(type=np.matrix)
    K = RT * [[x], [y], [1]]
    T = RT * [[tvct[0]], [tvct[1]], [tvct[2]]]
    zc = T[2, 0] / K[2, 0]
    W = zc * K - T
    return W[0, 0], W[1, 0]


def newpic2world(u, v):
    world_coord = np.array([[u], [v], [1]])
    world_coord = inv(cameraMatrix) * world_coord
    world_coord = world_coord * distance_cam
    world_x = world_coord[0][0]
    world_y = world_coord[1][1]
    print(world_x, world_y)
    return world_x, world_y


def world2picture(x, y):
    pnt, jac = cv2.projectPoints(np.array([[x, y, 0]], dtype=np.float32),
                                 rvct, tvct, cameraMatrix, distortionCoeffs)
    return pnt[0][0]


def mousecb(event, u, v, *arg):
    if event == cv2.EVENT_LBUTTONDOWN:
        x, y = picture2world(u, v)
        u1, v1 = world2picture(x, y)
        print(u, v, '=>', x, y, '=>', u1, v1)


def _testReverseTrans():
    global distortionCoeffs
    src = cv2.imread('3.jpg')
    # distortionCoeffs = np.array([0, 0, 0, 0, 0], dtype=np.float32)
    utils.utils.showimg_cb("P2W", src, mousecb)
