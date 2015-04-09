import cv2
import numpy as np
from matplotlib import pyplot as plt

class fft_filter():
    
    def __init__(self,imagePath):
        self.image = cv2.imread('lenna.jpg',0)
        f = np.fft.fft2(self.image)
        fshift = np.fft.fftshift(f)
        self.magnitudeSpec = 20*np.log(np.abs(fshift))
        self.phaseSpec = 20*np.log(np.angle(fshift))
        
    def graph(self):
        plt.subplot(141),plt.imshow(self.image, cmap = 'gray')
        plt.subplot(142),plt.imshow(self.magnitudeSpec, cmap = 'gray')
        plt.subplot(143),plt.imshow(self.phaseSpec, cmap = 'gray')
        plt.show()
        
        

        
if __name__ == "__main__":
    fft = fft_filter("lenna.jpg")
    fft.graph()