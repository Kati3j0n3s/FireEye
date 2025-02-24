# Import Libraries
import os
from picamzero import Camera

# Import Modules
import error_handler

class CameraControl:
    _instance = None

    def __init__(self, save_directory="/home/username/Pictures/test_images/test_image.jpg"):
        if CameraControl._instance is None:
            CameraControl._instance = Camera()
        self.camera = Camera()
        self.save_directory = save_directory

    def save_image(self, image_path):
        self.camera.take_photo(image_path)
        return os.path.exists(image_path)

    """Takes a test image to verify camera functionality."""
    def test_image(self):
        try:
            test_image_path = os.path.join(self.save_directory, "test_image.jpg")
            if self.save_image(test_image_path):
                print(f"Test image saved successfully: {test_image_path}")
                return True
            else:
                print("Failed to save the test image.")
                return False
        except Exception as e:
            error_handler.log_error(str(e), "CameraControl.test_image")
            return False
        
    def take_picture(self, image_path):
        try:
            if self.save_image(image_path):
                return True
            else:
                return False
        except Exception as e:
            error_handler.log_error(str(e), "CameraControl.take_picture")
            return False
