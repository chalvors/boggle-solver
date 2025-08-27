import sys
sys.path.insert(1, '../')
import detect
import cv2


image = cv2.imread(r'./images/boggle_3.jpg')

detector = detect.Detect()
processedImage = detector.preprocess_image(image)

cv2.imshow("input", image)
cv2.imshow("result", processedImage)
cv2.waitKey(0)
cv2.destroyAllWindows()