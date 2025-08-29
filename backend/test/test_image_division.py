import sys
sys.path.insert(1, '../')
from detect import Detect
import cv2
import unittest
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true", help="Show images for manual verification.")
args = parser.parse_args()

image = cv2.imread(r'./images/boggle_3.jpg')
detect = Detect()
processed_image = detect.preprocess_image(image)
cell_images = detect.divide_image(processed_image)


class TestImageDivision(unittest.TestCase):
    
    def test_image_division_cell_count(self):

        self.assertEqual(len(cell_images), 16)

    
    def test_image_division_cells_are_square(self):

        cell_shapes = []

        for cell_image in cell_images:
            cell_shapes.append(cell_image.shape)
        
        self.assertTrue(bool(len(set(cell_shapes)))) # Shapes of all cells are the same

    
    def test_image_division_show_cells(self):

        if (args.verbose):

            for cell_image in cell_images:
                cv2.imshow("cell", cell_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()



if __name__ == '__main__':
    unittest.main()