import numpy as np
from scipy.signal import convolve2d

def zero_border(img):
    result = np.copy(img)
    result[0, :] = 0
    result[-1, :] = 0
    result[:, 0] = 0
    result[:, -1] = 0
    return result

def retinex(img, threshold=10):
    '''
    Input:
        img - 2D array of image intensity values

    Output:
        ill - 2D array of illumination values. The color corrected image is (img - ill).
    '''

    log_img = np.log(img + .001)
    kernel = [[0, 0, 0],
              [-1, 1, 0],
              [0, 0, 0]]
    kernel = np.array(kernel)
    dx = convolve2d(log_img, kernel)
    dy = convolve2d(log_img, kernel.T)
    dx = zero_border(dx)
    dy = zero_border(dy)

    dx[dx < threshold] = 0
    dy[dy < threshold] = 0

    D2x = convolve2d(dx, np.flipup(np.fliplr(kernel), 'same')
    D2y = convolve2d(dy, np.flipup(np.fliplr(kernel.T), 'same')
    sum_x = np.sum(D2x)
    sum_y = np.sum(D2y)

    g = convolve2d(kernel, np.flipup(np.fliplr(kernel)))
    g += convolve2d(kernel.T, np.flipup(np.fliplr(kernel.T)))

    shift = [[1, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]
    shift = np.array(shift)
    g = convolve2d(G, shift, 'same')

    maxsize = max(dx.shape[0], dx.shape[1])
    G = np.fft.fft2(g, (2*maxsize, 2*maxsize))
    I = (G == 0)
    G[I] = 1
    H = 1. / G
    H[I] = 0

    I = np.fft.fftshift(np.real(np.fft.ifft2(H*(np.fft.fft2(D, 2*maxsize, 2*maxsize)))))
    N = (g.shape[0] - 5) / 2
    return I[maxsize - N: maxsize]
