from picamzero import Camera
import os
from datetime import datetime

def test_image(camera):
    """
    Takes a test image to verify that the camera is functional.
    """
    try:
        test_image_path = "/home/username/Pictures/test_images/test_image.jpg"  # Save to a known location
        camera.take_photo(test_image_path)
        if os.path.exists(test_image_path):
            print(f"Test image saved successfully: {test_image_path}")
            return True
        else:
            print("Failed to save the test image.")
            return False
    except Exception as e:
        print(f"Error during camera test: {e}")
        return False
        
def take_picture(camera, image_path):
	try:
		camera.take_photo(image_path)
		if os.path.exists(image_path):
			#print(f"Image saved successfully: {image_path}")
			return True
		else:
			#print(f"Failed to save the image at {image_path}")
			return False
	except Exception as e:
		print(f"Error taking picture: {e}")
		return False
