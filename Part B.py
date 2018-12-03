import numpy as np #import modules
import cv2
import math

img1 = cv2.imread('test3a.jpg', cv2.IMREAD_COLOR) #read in images in colour
intensity1 = cv2.imread('test3a.jpg', cv2.IMREAD_GRAYSCALE)#read in images in greyscale
img2 = cv2.imread('test3b.jpg', cv2.IMREAD_COLOR)
intensity2 = cv2.imread('test3b.jpg', cv2.IMREAD_GRAYSCALE)

#function for gaussian function
def gaussian(x,s):
    ans = (1.0/(math.sqrt(2*math.pi))*s)*(math.exp(-(x**2)/(2*(s**2))))
    return ans

#function to apply bilateral filter to image
def bilateral_filter(img):
    
    dim = 25 #parameters for size of neighbourhood and sigma values
    s1 = 120 #sigma for similarity
    s2 = 3 #sigma for distance
    filtered = [] #create array for filtered image
    
    for y in range(img.shape[0]): #for every row in image
        filtered.append([]) #add a list to the array
        
        for x in range(img.shape[1]): #for every pixel in image
            filtered[y].append(0) #add 0 to array
            numerator = 0 #initialise variables
            denom = 0
            
            for i in range(dim): #in the neighbourhood  
                for j in range(dim):
                    neighbour_x = x-(int((dim/2))-i) #find neighbour
                    neighbour_y = y-(int((dim/2))-j)
                    if neighbour_y >= len(img): #ensure neighbour in image
                        neighbour_y -= len(img)
                    if neighbour_x >= len(img[0]):
                        neighbour_x -= len(img[0])    
                    g1 = gaussian(img[y][x] - img[neighbour_y][neighbour_x],s1) #find gaussian value for similarity
                    g2 = gaussian(math.sqrt((x-neighbour_x)**2+(y-neighbour_y)**2),s2) #find gaussian value for distance
                    numerator += img[neighbour_y][neighbour_x]*g1*g2 #add to the numerator of the equation
                    denom += g1*g2 #add to the denominator of the equation
                    
            ans = numerator/denom #find the new pixel value
            filtered[y][x] = int(round(ans)) #add it to the array
            
    filtered = np.asarray(filtered) #make the array an nparray
    return filtered #return filtered image
            

if not img1 is None: #if both images exist
    if not img2 is None:
        
        intensity1 = cv2.cvtColor(intensity1,cv2.COLOR_GRAY2BGR) #change grayscale to colour for division
        err = np.seterr(all='ignore') #ignore inapplicable warning messages
        colour1 = np.divide(img1,intensity1) #divide image by intensity for colour
        intensity1 = cv2.cvtColor(intensity1,cv2.COLOR_BGR2GRAY) #change back to grayscale
        
        largescale1 = bilateral_filter(intensity1) #apply the bilateral filter to both intensity images for edge
        largescale2 = bilateral_filter(intensity2) #produces edge sharpened image

        detail2 = intensity2/largescale2 #find detail by dividing intensity image by edge sharpened image
        overall_intensity = largescale1*detail2 #multiply edge sharpened from no flash with detail from flash for overall intensity
        overall_intensity = np.uint8(overall_intensity) #make sure overall_intensity is correct type
        overall_intensity = cv2.cvtColor(overall_intensity,cv2.COLOR_GRAY2BGR) #make overall intensity colour image
        final = overall_intensity*colour1 #multiply overall intensity by colour for final image

        cv2.imwrite("final.png", final) #writing image to file
        print("finished") #inform user program over
        
else:
    print("No image file successfully loaded.") #inform user if no images
