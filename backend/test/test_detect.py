import sys
sys.path.insert(1, '../')
from detect import Detect
import cv2
import unittest


image = cv2.imread(r'./images/boggle_3.jpg')
detect = Detect()
board = detect.detect_letters(image)


class TestImageDivision(unittest.TestCase):

    def test_detect(self):
        detect.print_board(board)



if __name__ == '__main__':
    unittest.main()