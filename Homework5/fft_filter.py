import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt

class fft_filter():
    
    def __init__(self,imagePath):
        self.image = cv2.imread('lenna.jpg',0)
        (self.rows, self.columns) = self.image.shape
        self.paddedimage = self.__pad(self.image)
        self.__fft()
        
    def graph(self):
        plt.subplot(131),plt.imshow(self.image, cmap = 'gray')
        plt.subplot(132),plt.imshow(self.magnitudeSpec, cmap = 'gray')
        plt.subplot(133),plt.imshow(self.phaseSpec, cmap = 'gray')
        plt.show()
        
    def __pad(self,image):
        padded_image = np.zeros((2*self.rows,2*self.columns), dtype=np.int)
        for row in range(self.rows):
            for column in range(self.columns):
                padded_image[row][column] = image[row][column]

        
        return padded_image        
        #im = Image.fromarray(np.uint8(padded_image))
        #im.convert('RGB').save("padded.jpg")
        
    def __fft(self):
        self.fft = np.fft.fft2(self.paddedimage)
        fshift = np.fft.fftshift(self.fft)
        self.magnitudeSpec = 20*np.log(np.abs(fshift))
        self.phaseSpec = 20*np.log(np.angle(fshift))
        
    def idealLowpassFilter(self,frequency=100):
        filter = np.zeros((2*self.rows, 2*self.columns), dtype=np.int)
        a = self.rows / 2
        b = self.columns / 2

        for row in range(self.rows):
            for column in range(self.columns):
                if ((row - a) ** 2 + (column - b) ** 2 <= frequency ** 2):
                    filter[row + a][column + b] = 1
        
    

        
if __name__ == "__main__":
    fft = fft_filter("lenna.jpg")
    #fft.graph()
    fft.idealLowpassFilter()