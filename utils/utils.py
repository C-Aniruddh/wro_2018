import numpy as np
import cv2
from PIL import Image
import numpy as np
from io import BytesIO


def scale(im, size=128):
    '''
    accepts: PIL image, size of square sides
    returns: PIL image scaled so sides lenght = size
    '''
    size = (size, size)
    im.thumbnail(size, Image.ANTIALIAS)
    return im


def img_to_binary(img):
    '''
    accepts: PIL image
    returns: binary stream (used to save to database)
    '''
    f = BytesIO()
    img.save(f, format='jpeg')
    return f.getvalue()


def arr_to_binary(arr):
    '''
    accepts: numpy array with shape (Hight, Width, Channels)
    returns: binary stream (used to save to database)
    '''
    img = arr_to_img(arr)
    return img_to_binary(img)


def arr_to_img(arr):
    '''
    accepts: numpy array with shape (Hight, Width, Channels)
    returns: binary stream (used to save to database)
    '''
    arr = np.uint8(arr)
    img = Image.fromarray(arr)
    return img


def img_to_arr(img):
    '''
    accepts: numpy array with shape (Hight, Width, Channels)
    returns: binary stream (used to save to database)
    '''
    return np.array(img)


def binary_to_img(binary):
    '''
    accepts: binary file object from BytesIO
    returns: PIL image
    '''
    img = BytesIO(binary)
    return Image.open(img)


def norm_img(img):
    return (img - img.mean() / np.std(img)) / 255.0


def rgb2gray(rgb):
    '''
    take a numpy rgb image return a new single channel image converted to greyscale
    '''
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])


def map_range(x, X_min, X_max, Y_min, Y_max):
    '''
    Linear mapping between two ranges of values
    '''
    X_range = X_max - X_min
    Y_range = Y_max - Y_min
    XY_ratio = X_range / Y_range

    y = ((x - X_min) / XY_ratio + Y_min) // 1

    return int(y)


def get_limits(red, green, blue):
    color = np.uint8([[[blue, green, red]]])
    hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
    hue = hsv_color[0][0][0]
    print("Lower limit : [{}, 100, 100]".format(hue - 10))
    print("Upper limit  : [{}, 255, 255]".format(hue + 10))
    lower_limit = np.array([hue - 10, 100, 100])
    upper_limit = np.array([hue + 10, 255, 255])
    return lower_limit, upper_limit


def __normalize_image(image):
    if image.dtype == np.bool:
        return image.astype(np.uint8) * 255
    else:
        return image


def showimg(*arg, **kw):
    for k, v in enumerate(arg):
        cv2.imshow(str(k), __normalize_image(v))
    for k, v in kw.items():
        cv2.imshow(k, __normalize_image(v))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def showimg_cb(title, image, cb):
    cv2.namedWindow(title)
    cv2.setMouseCallback(title, cb)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyWindow(title)


def dumpimg(path, **kw):
    base, ext = path.rsplit('.', 1)
    for k, v in kw.items():
        cv2.imwrite('{}.{}.{}'.format(base, k, ext), __normalize_image(v))
