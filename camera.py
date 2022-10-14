import picamera
from time import sleep
import upload
camera = picamera.PiCamera()
camera.vflip = True
def preview(rt):
    camera.start_preview()
    sleep(rt)
    camera.stop_preview()
    camera.close()
def image(image):
    print("Picture in 3")
    sleep(1)
    print("2")
    sleep(1)
    print("1")
    sleep(1)
    print("Now!")
    camera.capture(image)
def video(video):
    print("Video starts in 3")
    sleep(1)
    print("2")
    sleep(1)
    print("1")
    sleep(1)
    print("Now!")
    camera.start_recording(video)
    sleep(10)
    camera.stop_recording()
def upload():
    camera.start_preview()
    sleep(5)
    camera.capture('/home/pi/python/image.jpg')
    camera.end_preview()
    camera.close()
    uppic = upload.Upload()
    uppic.picture('', '', '',
                  'Grant', '/home/pi/python/image.jpg', 'image.jpg',
                  permission=False)
