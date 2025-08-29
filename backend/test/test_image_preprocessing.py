import sys
sys.path.insert(1, '../')
from detect import Detect
import cv2
import unittest
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true", help="Show images for manual verification.")
args = parser.parse_args()


image = cv2.imread(r'./images/boggle_2.jpg')
detect = Detect()
processed_image = detect.preprocess_image(image)


class TestImagePreprocessing(unittest.TestCase):

    def test_image_preprocessing_grayscale(self):

        if processed_image.ndim == 2:
            pass
        else:
            raise AssertionError("processed image is not grayscale")
        

    def test_image_preprocessing_square(self):

        (processed_image_height, processed_image_width) = processed_image.shape
        self.assertEqual(processed_image_height, processed_image_width)  # Processed image is a square

    
    def test_image_preprocessing_show_before_and_after(self):

        if (args.verbose):
            cv2.imshow("input", image)
            cv2.imshow("result", processed_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()



if __name__ == '__main__':
    unittest.main()

