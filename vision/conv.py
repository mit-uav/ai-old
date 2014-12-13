import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
from scipy.signal import convolve2d, fftconvolve
from scipy.ndimage.filters import gaussian_filter, gaussian_laplace
import os
import cv2

def ellipse((center_i, center_j), (r_i, r_j), (height, width)):
    r_i = float(r_i)
    r_j = float(r_j)
    y = np.arange(-center_i, height-center_i)[np.newaxis].T
    x = np.arange(-center_j, width-center_j)
    mask = x*x / r_j**2 + y*y / r_i**2
    return (mask <= 1)


def test():
    cap = cv2.VideoCapture('videos/roomba.mp4')
    # width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    # height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    flag, frame = cap.read()
    frame = np.mean(frame, axis=2)
    frame = frame[::10,::10]
    height, width = frame.shape

    fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
    writer = cv2.VideoWriter('result.mp4', fourcc, fps, (width, height), True)

    # (center_i, center_j) = (894, 515)
    # (r_i, r_j) = (300, 310)
    (center_i, center_j) = (89, 52)
    (r_i, r_j) = (30, 31)

    mask = ellipse((center_i, center_j), (r_i, r_j), frame.shape)
    kernel = frame * mask

    for count in range(1000):
    # count = 0
    # while flag:
    #     count += 1
        print count
        flag, frame = cap.read()
        frame = frame[::10, ::10, :]
        grey = np.mean(frame, axis=2)
        res = fftconvolve(grey, kernel, mode='same')
        index = np.argmax(res)
        (i, j) = np.unravel_index(index, res.shape)
        # if (40 < i < height - 40) and (40 < j < width - 40):
        #     frame[i-40:i+40,j-15:j+15,:] = 0
        #     frame[i-15:i+15,j-40:j+40,:] = 0

        if (6 < i < height - 6) and (6 < j < width - 6):
            frame[i-6:i+6,j-2:j+2,:] = 0
            frame[i-2:i+2,j-6:j+6,:] = 0
        # plt.imshow(frame)
        # plt.show()
            writer.write(frame)

    writer.release()

if __name__ == '__main__':
    test()
