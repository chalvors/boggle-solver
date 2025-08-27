import sys
sys.path.insert(1, '../')
from detect import Detect
import cv2

image = cv2.imread(r'./images/boggle_3.jpg')

detect = Detect()
processedImage = detect.preprocess_image(image)
cells = detect.divide_image(processedImage)

for cell in cells:
    cv2.imshow("cell", cell)
    cv2.waitKey(0)
    cv2.destroyAllWindows()