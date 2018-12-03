import numpy as np
import cv2

windowName = "Image"; 

img = cv2.imread('test2.png', cv2.IMREAD_COLOR);

if not img is None:

    
    blur = cv2.bilateralFilter(img,25,50,7);

    cv2.imshow(windowName, blur);
    cv2.imwrite("result1.png",blur)

    key = cv2.waitKey(0);

    if (key == ord('x')):
        cv2.destroyAllWindows();
else:
    print("No image file successfully loaded.");


