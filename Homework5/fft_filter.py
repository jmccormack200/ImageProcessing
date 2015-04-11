import Image
import cv2
import numpy as np
import math
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
        self.fshift = np.fft.fftshift(self.fft)
        self.magnitudeSpec = 20*np.log(np.abs(self.fshift))
        self.phaseSpec = 20*np.log(np.angle(self.fshift))
        im = Image.fromarray(np.uint8(self.magnitudeSpec))
        im.convert('RGB').save("FFT.jpg")
        
    def idealLowpassFilter(self,frequency):
        self.idealFilter(frequency)
        
    def idealHighpassFilter(self,frequency):
        self.idealFilter(frequency,False)
        
    def gaussianLowpassFilter(self,frequency):
        self.gaussianFilter(frequency)
    
    def gaussianHighpassFilter(self,frequency):
        self.gaussianFilter(frequency,False)
        
    def idealFilter(self,frequency,low=True):
        filter = np.zeros((2*self.rows, 2*self.columns), dtype=np.int)
        cropped = np.zeros((self.rows, self.columns), dtype = np.int)
        
        a = self.rows / 2
        b = self.columns / 2

        for row in range((-1*self.rows),self.rows):
            for column in range((-1*self.columns),self.columns):
                if low:
                    if (((row - a) ** 2) + ((column - b) ** 2) <= frequency ** 2):
                        filter[row + a][column + b] = 1
                else:
                    if (((row - a) ** 2) + ((column - b) ** 2) >= frequency ** 2):
                        filter[row + a][column + b] = 1

        outputFFT = np.multiply(self.fshift, filter)

        im = Image.fromarray(np.uint8(20*np.log(np.abs(outputFFT))))
        if low:
            im.convert('RGB').save("IdealLPFFT.jpg")
        else:
            im.convert('RGB').save("IdealHPFFT.jpg")
        
        outputImage = np.fft.ifftshift(outputFFT)
        outputImage = np.fft.ifft2(outputImage)
        
        for row in range(self.rows):
            for column in range(self.columns):
                cropped[row][column] = abs(outputImage[row][column])
        
        im = Image.fromarray(np.uint8(cropped))
        if low:
            im.convert('RGB').save("IdealLP.jpg")
        else:
            im.convert('RGB').save("IdealHP.jpg")

    def gaussianFilter(self, frequency, low=True):
        filter = np.zeros((2*self.rows, 2*self.columns), dtype=np.float)
        cropped = np.zeros((self.rows, self.columns), dtype = np.int)
        
        a = self.rows
        b = self.columns
        highLow = 0 if low else 1
        
        for row in range((-1*self.rows),self.rows):
            for column in range((-1*self.columns),self.columns):
                distance = math.sqrt(row**2 + column**2)
                filter[row + a][column + b] = highLow - (math.exp(-1.0*distance/((2.0*frequency)**2.0)))

        outputFFT = np.multiply(self.fshift, filter)

        im = Image.fromarray(np.uint8(20*np.log(np.abs(outputFFT))))
        if low:
            im.convert('RGB').save("GaussianLPFFT.jpg")
        else:
            im.convert('RGB').save("GaussianHPFFT.jpg")
        
        outputImage = np.fft.ifftshift(outputFFT)
        outputImage = np.fft.ifft2(outputImage)
        
        for row in range(self.rows):
            for column in range(self.columns):
                cropped[row][column] = abs(outputImage[row][column])
        
        im = Image.fromarray(np.uint8(cropped))
        if low:
            im.convert('RGB').save("GaussianLP.jpg")
        else:
            im.convert('RGB').save("GaussianHP.jpg")
            
    def laplacianFilter(self):
        filter = np.zeros((2*self.rows, 2*self.columns), dtype=np.int)
        cropped = np.zeros((self.rows, self.columns), dtype = np.int)
    
        a = self.rows
        b = self.columns
    
        for row in range(self.rows * 2):
            for column in range(self.columns * 2):
                filter[row][column] = 1-(((row - a)**2 + (column - b)**2))


        #outputFFT = np.multiply(self.fshift, filter)
        
        im = Image.fromarray(np.uint8(filter))
        im.convert('RGB').save("test.jpg")
        '''
        im = Image.fromarray(np.uint8(20*np.log(np.abs(outputFFT))))
        im.convert('RGB').save("LaplacianFFT.jpg")

        
        outputImage = np.fft.ifftshift(outputFFT)
        outputImage = np.fft.ifft2(outputImage)
        
        for row in range(self.rows):
            for column in range(self.columns):
                cropped[row][column] = abs(outputImage[row][column])
        
        im = Image.fromarray(np.uint8(outputImage))
        im.convert('RGB').save("Laplacian.jpg")
        '''
        
        
if __name__ == "__main__":
    fft = fft_filter("lenna.jpg")
    #fft.graph()
    #fft.idealLowpassFilter(50)
    #fft.idealHighpassFilter(20)
    #fft.gaussianLowpassFilter(10)
    #fft.gaussianLowpassFilter(2)
    #fft.gaussianHighpassFilter(5)
    fft.laplacianFilter()
