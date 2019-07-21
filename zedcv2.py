import numpy as np
import cv2

class Camera():
    def __init__(self,):
        self.cap = cv2.VideoCapture(1)

        # Default resolution 2K
        self.set_resolution("2K")
        # Default using left eye
        self.set_eye("left")

    def __del__(self,):
        self.cap.release()

    def set_resolution(self, resolution):
        if resolution == "2K":
            width = 4416
            height = 1242
        elif resolution == "1080p":
            width = 3840
            height = 1080
        elif resolution == "720p":
            width = 2560
            height = 720
        elif resolution == "WVGA":
            width = 1344
            height = 376
        else:
            print("Unsupported resolution type")
            raise NameError

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        self._width = width
        self._height = height


    def set_eye(self, eye):
        assert eye in ["left", "right", "both"], "Unsupported type"
        self._eye = eye
       

    def open(self,):
        pass

    def retrieve_image(self,):
        ret, frame = self.cap.read()
        print(frame.shape)   
        
        if ret:
            if self._eye == "left":
                frame = frame[:, :int(self._width/2), :]
            elif self._eye == "right":
                frame = frame[:, int(self._width/2):, :]
            elif self._eye == "both":
                frame = frame
            else:
                raise NotImplementedError

            return frame
        else:
            print("Can't reach image.")
            return 0

    

        
if __name__ == "__main__":
    zed = Camera()
    zed.set_resolution("WVGA")
    zed.set_eye("left")


    while(True):
        # Capture frame-by-frame
        frame = zed.retrieve_image()

        # # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break