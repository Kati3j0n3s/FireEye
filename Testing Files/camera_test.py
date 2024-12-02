# from picamzero import Camera
# from time import sleep

# cam = Camera()
# cam.start_preview()
# # Keep the preview window open for 5 seconds
# sleep(5)

from picamzero import Camera

cam = Camera()
cam.start_preview()
cam.take_photo("/home/username/Pictures/new_image.jpg")
cam.stop_preview()
