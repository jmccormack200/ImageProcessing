import Image
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np

#################
#
# Histogram Array
#
# Inputs: 
#   pix - pixel information
#   width - Width of the image
#   height - height of the image
#
# Outputs: 
#   output_array - a 2D array containing
#   the number of pixels that are at
#   that grey scale value.
#
#################
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

#################
#
# Normalize Array
#
# Inputs: 
#   array - the array returned from 
#           Histogram Array
#   width - Width of the image
#   height - height of the image
#
# Outputs: 
#   array - The array normalized
#           to the number of pixels in
#           the image.
#
#################
def normalize_array(array, width, height):
    total_pixels = width * height
    total_pixels = float(total_pixels)
    for number in range(len(array)):
        array[number] = array[number]/total_pixels
    return array

#################
#
# CDF Array
#
# Inputs: 
#   array - the array returned from 
#           normailze array
#
# Outputs: 
#   array - An Array representing
#           the CDF of the image
#
#################    
def Cdf_Array(array):
    output_array = []
    total_number = 0
    for number in array:
        number = number * 255
        total_number += number
        output_array.append(total_number)
    return output_array

#################
#
# CDF Array
#
# Inputs: 
#   array - The CDF of the function
# Outputs: 
#   array - The CDF Rounded
#
#################    
def rounding(array):
    for number in range(len(array)):
        array[number] = int(round(array[number]))
    return array
    
#################
#
# Probability Output
#
# Inputs: 
#   rounded_array - the array returned from 
#                   rounding function
#   probability_array - the array returned
#                       from the normalize
#                       function.
#   width - Width of the image
#   height - height of the image
#
# Outputs: 
#   array - The probablity, normalized by the
#           CDF.
#################
def probability_output(rounded_array, probability_array, width, height):
    total_pixels = height * width
    output_array = []

    for a in range(0,256):
        output_array.append(0)
    
    for number in range(len(array)):
        output_array[rounded_array[number]] += probability_array[number]
    return output_array
#################
#
# Edit Image
#
# Inputs: 
#   pix - the pixel information 
#   array - the array used
#           to make the transformation
#   width - Width of the image
#   height - height of the image
#
# Outputs: 
#   The image is edited according to
#   the new array.
#################    
def edit_image(pix, array, width, height):
    for x in range(width):
        for y in range(height):
            old_value = pix[x,y]
            new_value = array[old_value[0]]
            pix[x,y] = new_value

#################
# Plot Histogram
#   
# Inputs:
#   array1-array4 - the 4 arrays to print out
#   count - The number to append to the output name
#
# Outputs:
#   The plots are saved as "output#.png"
#
#################
def plot_histogram(array1, array2, array3, array4, count):
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
    plt.savefig('output' + str(count) + 'png')

#################
# Plot All CDFs
#
# Inputs:
#   cdf_array - all of the CDFs
#
# Outputs:
#   The plots are saved as "all_cdfs.png"
#
#################    
def plot_all_cdfs(cdf_array):
    ind = np.arange(256)
    fig = plt.figure()
    plt.title("Plot of all CDFs")
    plt.xlabel("Pixel Color")
    plt.ylabel("Probablity")
    plt.plot(ind, cdf_array[0], 'r--', ind, cdf_array[1], 'bs', ind, cdf_array[2], 'g^', ind, cdf_array[3], 'b^')
    plt.savefig('all_cdfs.png')
   

if __name__ == '__main__':
    #Create a blank image to hold the four transformed images
    output_img = Image.new("RGB", (3840,2160))
    
    #initialize an array to hold the images, and one to hold cdfs
    img_array = []
    all_cdfs = []
    
    #open the four images and add to image array
    img_array.append(Image.open("Boston_Bright.bmp").convert("LA"))
    img_array.append(Image.open("Boston_Dark.bmp").convert("LA"))
    img_array.append(Image.open("Boston_Low.bmp").convert("LA"))
    img_array.append(Image.open("Boston_High.bmp").convert("LA"))
    
    #create a counter
    output_number = 0
    
    #for each image in the array
    for img in img_array:    
        #Load the image
        pix = img.load()
        #set the width and the height to be that of the image
        (width, height) = img.size
        #first find the sum of each pixel value
        array = histogram_array(pix, width, height)
        #Then find the probability based on the pixels
        probability_array = normalize_array(array, width, height)
        #Generate the CDF
        cdf_array = Cdf_Array(probability_array)
        #Append this for graphing later.
        all_cdfs.append(cdf_array)
        #round the CDF to the nearest whole number
        round_array = rounding(cdf_array)
        #Edit the image to even out the colors
        pix = edit_image(pix, round_array, width, height)
        #append the image to the image array
        img_array[output_number] = img.convert("RGB")
        #find the new probability of each pixel
        final_array = probability_output(round_array, probability_array, width, height)
        #find the new cdf
        final_array_cdf = Cdf_Array(final_array, width, height)
        #print out the original probability, original cdf, new probability, and new CDF
        plot_histogram(probability_array, cdf_array, final_array, final_array_cdf, output_number)
        #increase control variable by 1
        output_number += 1
    #plot all the CDFs on one plot
    plot_all_cdfs(all_cdfs)
    
    #plot all pictures next to each other
    output_img.paste(img_array[0], (0,0))
    output_img.paste(img_array[1], (1920,0))
    output_img.paste(img_array[2], (0, 1080))
    output_img.paste(img_array[3], (1920,1080))
    output_img.save("output.bmp")
    