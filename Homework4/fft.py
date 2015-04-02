"""

Adapted from OpenCV Documentation

"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('lenna.jpg',0)
img2 = cv2.imread('skulldftPower.jpg',0)
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)


magnitude_spectrum = 20*np.log(np.abs(fshift))
img3 = abs(img2 - magnitude_spectrum)
plt.subplot(141),plt.imshow(img, cmap = 'gray')
plt.subplot(142),plt.imshow(magnitude_spectrum, cmap = 'gray')
plt.subplot(143),plt.imshow(img2, cmap = 'gray')
plt.subplot(144),plt.imshow(img3, cmap = 'gray')
plt.show()
