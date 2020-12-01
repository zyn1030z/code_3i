import cv2
import imutils
import globals

class Capture(object):
    def __init__(self, video_source):
        # Open the video source
        self.vid = imutils.video.VideoStream(src=video_source).start()
        if not self.vid:
            raise ValueError("Unable to open video source", video_source)

    def get_frame(self):
        if self.vid:
            frame = self.vid.read()
            if globals.extract==0:
                frame = imutils.resize(frame, width=600)
            return frame

    def __del__(self):
        if self.vid:
            self.vid.stop()
        cv2.destroyAllWindows()
        print('destroy_Cam')    