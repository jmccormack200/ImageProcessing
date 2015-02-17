import Image
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np

def  histogram_array (pix, width, height):
    output_array = []
    total = 0
    for a in range(0,256):
        output_array.append(0)
    for x in range(width):
        for y in range(height):
            grey = pix[x,y]
            output_array[grey[0]] = output_array[grey[0]] + 1
    return output_array

def normalize_array(array, width, height):
    total_pixels = width * height
    total_pixels = float(total_pixels)
    for number in range(len(array)):
        array[number] = array[number]/total_pixels
    return array
    
def Cdf_Array(array, width, height):
    output_array = []
    total_number = 0
    for number in array:
        number = number * 255
        total_number += number
        output_array.append(total_number)
    return output_array

def rounding(array, width, height):
    for number in range(len(array)):
        array[number] = int(round(array[number]))
    return array

def probability_output(rounded_array, probability_array, width, height):
    total_pixels = height * width
    output_array = []

    for a in range(0,256):
        output_array.append(0)
    
    for number in range(len(array)):
        output_array[rounded_array[number]] += probability_array[number]
    return output_array
    
def edit_image(pix, array, width, height):
    for x in range(width):
        for y in range(height):
            old_value = pix[x,y]
            new_value = array[old_value[0]]
            pix[x,y] = new_value

def plot_histogram(array1, array2, array3, array4):
    ind = np.arange(256)
    fig = plt.figure()
    ax = plt.subplot(411)
    rects1 = ax.bar(ind, array1, color='r')
    ax = plt.subplot(412)
    rects2 = ax.bar(ind, array2, color='b')
    ax = plt.subplot(413)
    rects3 = ax.bar(ind, array3, color='g')
    ax = plt.subplot(414)
    rects4 = ax.bar(ind, array4, color='y')
    plt.show()
    
    

if __name__ == '__main__':
    img = Image.open("lena.bmp").convert("LA")
    pix = img.load()
    (width, height) = img.size
    array = histogram_array(pix, width, height)
    probability_array = normalize_array(array, width, height)
    cdf_array = Cdf_Array(probability_array, width, height)
    round_array = rounding(cdf_array, width, height)
    pix = edit_image(pix, round_array, width, height)
    img.convert("RGB").save("output.jpg")
    final_array = probability_output(round_array, probability_array, width, height)
    final_array_cdf = Cdf_Array(final_array, width, height)
    plot_histogram(probability_array, cdf_array, final_array, final_array_cdf)

    