import cv2

class ImageProcessor:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    def denoise(self):
        self.image = cv2.fastNlMeansDenoising(self.image, None, 10, 7, 21)
        return self

    def adaptive(self):
        self.image = cv2.adaptiveThreshold(self.image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        return self

    def resize(self):
        height, width = self.image.shape
        new_width = 1000
        aspect_ratio = width / height
        new_height = int(new_width / aspect_ratio)
        self.image = cv2.resize(self.image, (new_width, new_height))
        return self

    def get_image(self):
        return self.image

    def show_image(self, window_name='receipts_training'):
        cv2.imshow(window_name, self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
