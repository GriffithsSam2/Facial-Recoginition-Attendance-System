import os
import cv2
import face_recognition

from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QThread, Signal

from AttendanceAdmin_Resource__ut import wait
from AttendanceAdmin_Resource__ed import Attendance


class CaptureHandler(QThread):
    state = Signal(bool)

    def run(self):
        while True:
            self.state.emit(True)
            wait(30000)


class CaptureFace:
    def __init__(self) -> None:
        self.exit_ = False
        self.state = False
        self.image: str
        self.cam = None

        self.ch = CaptureHandler()
        self.ch.state.connect(self.set_state)

    def run(self):
        self.ch.start()

        self.cam = cv2.VideoCapture(0)
        img_counter = 0
        
        cv2.namedWindow("Capture face")
        face_locations = []
        
        while not self.exit_:
            ret, frame = self.cam.read()
            
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_frame = frame[:, :, ::-1]

            # Find all the faces in the current frame of video
            face_locations = face_recognition.face_locations(rgb_frame)

            # Display the results
            for top, right, bottom, left in face_locations:
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            if not ret:
                mb = QMessageBox()
                mb.setIcon(QMessageBox.Critical)
                mb.setText('Failed to grab capturing frame.')
                mb.setWindowTitle('Error')
                mb.show()

                break
            
            cv2.imshow('Capture face', frame)
            k = cv2.waitKey(60)

            if self.state:
                self.image = "temp/unknown.jpg"

                cv2.imwrite(self.image, frame)

                res = Attendance.record()

                mb = QMessageBox()
                mb.setIcon(QMessageBox.Information)

                if res:
                    mb.setText('Verification was successful.')
                else:
                    mb.setText('Verification failed.')

                mb.setWindowTitle('Result')
                mb.show()

                self.state = False
                img_counter += 1
        
        self.cam.release()
        cv2.destroyAllWindows()

    def set_state(self, state):
        self.state = state

    def terminate_(self):
        cv2.destroyAllWindows()


"""if __name__ == '__main__':
    app = QApplication([])

    cp = CaptureFace()

    

    cp.run()

    sys.exit(app.exec_())
"""