import sys
sys.path.insert(1, '../')
from detect import Detect
import cv2

def test_detect():
    
    image = cv2.imread(r'./images/boggle_3.jpg')
    detect = Detect()

    board = detect.detect_letters(image)
    detect.print_board(board)

if __name__ == '__main__':
    test_detect()