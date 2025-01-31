# Import Libraries
import os
from picamzero import Camera

# Import Modules
import error_handler

class CameraControl:
    def __init__(self):
        self.camera = Camera()

    """Takes a test image to verify camera functionality."""
    def test_image(self):
        try:
            test_image_path = "/home/username/Pictures/test_images/test_image.jpg"
            self.camera.take_photo(test_image_path)
            if os.path.exists(test_image_path):
                print(f"Test image saved successfully: {test_image_path}")
                return True
            else:
                print("Failed to save the test image.")
                return False
        except Exception as e:
            error_handler.log_error("Failed to save the test image", "test_image")
            return False
        
    def take_picture(self, image_path):
        try:
            self.camera.take_photo(image_path)
            if os.path.exists(image_path):
                return True
            else:
                return False
        except Exception as e:
            error_handler.log_error("Camera capture error", "take_picture")
            return False
