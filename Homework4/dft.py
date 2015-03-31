import Image
import numpy as np
from cmath import exp, pi, sqrt, atan

class DFT:
    
    def __init__(self, imagePath):
        self.image = Image.open(imagePath).convert("L")
        (self.width, self.height) = self.image.size
        self.pix = np.asarray(self.image)
        
    def takeDft(self):
        outputPower = np.empty([self.height, self.width])
        outputPhase = np.empty([self.height, self.width])
        
        for u in range(self.width):
            for v in range(self.height):
                complex = self.computePoint(u,v)
                outputPower[v][u] = sqrt((complex.real)**2 + (complex.imag)**2).real
                print complex
                outputPhase[v][u] = atan(complex.imag/complex.real).real
            print u
        
        outputDFT_im = Image.fromarray(outputPower)
        outputDFT_im.convert('RGB').save("dftPower.jpg")
            
    def computePoint(self,u,v):
        outputPoint = 0
        for x in range(self.width):
            for y in range(self.height):
                outputPoint += self.pix[y][x] * exp(-1j*pi*
                        (((u*x)/self.width) + ((v*y)/self.height)))
        return outputPoint       


if __name__ == "__main__":
    imagePath = "skull.gif"
    #imagePath = "cln1.gif"
    #imagePath = "360e.png"
    dft = DFT(imagePath)
    dft.takeDft()
    