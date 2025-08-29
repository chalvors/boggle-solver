import sys
sys.path.insert(1, '../')
from detect import Detect
import cv2
import unittest
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true", help="Show images for manual verification.")
args = parser.parse_args()


image = cv2.imread(r'./images/boggle_3.jpg')
detect = Detect()
board = detect.detect_letters(image)


class TestImageDivision(unittest.TestCase):

    def test_detect_board_size(self):

        np_arr = np.array(board)
        self.assertEqual(np_arr.shape, (4,4))


    def test_detect_print_board(self):

        if (args.verbose):
            detect.print_board(board)



if __name__ == '__main__':
    unittest.main()