import sys
sys.path.insert(1, '../')
import detect
import cv2

image = cv2.imread(r'C:\Users\darth\OneDrive\Desktop\dev\boggle-solver\backend\test\Boggle-Game-Board-Free.jpg')

processedImage = detect.preprocess_image(image)
cells = detect.divide_image(processedImage)

for cell in cells:
    cv2.imshow("cell", cell)
    cv2.waitKey(0)
    cv2.destroyAllWindows()