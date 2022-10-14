import upload
from picamera import PiCamera
c = PiCamera()
c.start_preview()
c.capture('/home/pi/upload/image.jpg')
c.stop_preview()
c.close()
pic = upload.Upload()
pic.picture('', '', ',
                    'Grant', '/home/pi/upload/image.jpg', 'image.jpg',
                    permission=False)
