import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QImage
import mediapipe
import pyautogui

class HandTrackingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hand Movement Tracking")
        self.setGeometry(100, 100, 800, 600)
        
        self.label = QLabel(self)
        self.label.setGeometry(10, 10, 640, 480)

        self.capture_hands = mediapipe.solutions.hands.Hands()
        self.drawing_option = mediapipe.solutions.drawing_utils
        self.screen_width, self.screen_height = pyautogui.size()
        self.camera = cv2.VideoCapture(0)
        self.x1 = self.y1 = self.x2 = self.y2 = 0
        self.timerEvent(None)
        self.startTimer(100)

    def timerEvent(self, event):
        _, image = self.camera.read()
        image_height, image_width, _ = image.shape
        image = cv2.flip(image, 1)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        output_hands = self.capture_hands.process(rgb_image)
        all_hands = output_hands.multi_hand_landmarks
        if all_hands:
            for hand in all_hands:
                self.drawing_option.draw_landmarks(image, hand)
                one_hand_landmarks = hand.landmark
                for id, lm in enumerate(one_hand_landmarks):
                    x = int(lm.x * image_width)
                    y = int(lm.y * image_height)
                    if id == 8:
                        mouse_x = int(self.screen_width / image_width * x)
                        mouse_y = int(self.screen_height / image_height * y)
                        cv2.circle(image,(x,y),10,(0,255,255))
                        pyautogui.moveTo(mouse_x,mouse_y)
                        self.x1 = x
                        self.y1 = y
                    if id == 4:
                        cv2.circle(image,(x,y),10,(0,255,255))
                        self.x2 = x
                        self.y2 = y
                dist = self.y2 - self.y1
                print(dist)
                if dist < 40:
                    pyautogui.click()
                    print("clicked")

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = image.shape
        bytes_per_line = ch * w
        q_img = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.label.setPixmap(pixmap)

    # def closeEvent(self, event):
    #     self.camera.release()
    #     cv2.destroyAllWindows()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HandTrackingWindow()
    window.show()
    sys.exit(app.exec_())
