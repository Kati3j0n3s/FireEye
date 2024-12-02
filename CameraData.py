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
			print(f"Image saved successfully: {image_path}")
			return True
		else:
			print(f"Failed to save the image at {image_path}")
			return False
	except Exception as e:
		print(f"Error taking picture: {e}")
		return False

	
    # """
    # Captures an image and saves it in a folder corresponding to the flight.

    # Parameters:
    # - base_directory (str): The root directory for storing all flight images (e.g., 'FireEye Images').
    # - flight_name (str): The name of the flight (e.g., 'Flight 001').
    # - image_name (str, optional): Name for the image file. If not provided, uses a timestamp.

    # Returns:
    # - str: The full path to the saved image, or None if an error occurs.
    # """
    # # Construct the directory for the specific flight
    # flight_directory = os.path.join(base_directory, flight_name)

    # try:
        # # Ensure the flight directory exists
        # os.makedirs(flight_directory, exist_ok=True)

        # # Generate a default image name if none is provided
        # if not image_name:
            # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # image_name = f"image_{timestamp}.jpg"

        # # Construct the full image path
        # image_path = os.path.join(flight_directory, image_name)

        # # Capture the image using the camera
        # Camera.take_photo(image_path)

        # # Verify that the image was saved successfully
        # if os.path.exists(image_path):
            # print(f"Image saved successfully: {image_path}")
            # return image_path
        # else:
            # print("Failed to save the image.")
            # return None

    # except Exception as e:
        # print(f"Error capturing image: {e}")
        # return None
        
        
	
