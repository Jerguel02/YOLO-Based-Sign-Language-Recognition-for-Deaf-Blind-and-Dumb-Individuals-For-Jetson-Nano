import sys
import os
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QEventLoop
import wave
import pyaudio

class AudioRecorder(QThread):
    signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.audio_filename = "audio/AUDIO.wav"
        self.recording = False
        self.recognizer = sr.Recognizer()
        self.CHUNK = 2048
        self.SAMPLE_FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.FS = 44100
        self.DURATION = 9

    def run(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.SAMPLE_FORMAT,
                        channels=self.CHANNELS,
                        rate=self.FS,
                        frames_per_buffer=self.CHUNK,
                        input=True)
        frames = []
        for _ in range(0, int(self.FS / self.CHUNK * self.DURATION)):
            if self.recording:
                data = stream.read(self.CHUNK)
                frames.append(data)
            else:
                break
        stream.stop_stream()
        stream.close()
        p.terminate()
    
        with wave.open(self.audio_filename, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(p.get_sample_size(self.SAMPLE_FORMAT))
            wf.setframerate(self.FS)
            wf.writeframes(b''.join(frames))
    
        recognized_text = self.recognize_speech(self.audio_filename)
        self.signal.emit(recognized_text)
    def stop_recording(self):
        print("Thread is terminating...")
        self.recording = False

    def recognize_speech(self, filename):
        with sr.AudioFile(filename) as source:
            audio_data = self.recognizer.record(source)
            try:
                text = self.recognizer.recognize_google(audio_data)
                print("Recognized text:", text)
                return text
            except (sr.UnknownValueError, sr.RequestError) as e:
                print(f"Speech recognition error: {e}")
                return ""

class YOLO_GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Voice Recorder & Sign Language GUI")
        self.setGeometry(100, 100, 800, 600)

        self.sign_language_label = QLabel(self)
        self.sign_language_label.setAlignment(Qt.AlignCenter)

        self.recording_label = QLabel("Recording...", self)
        self.recording_label.setAlignment(Qt.AlignCenter)
        self.recording_label.setVisible(False)

        self.record_button = QPushButton("Record", self)
        self.record_button.setMaximumHeight(30)
        self.record_button.clicked.connect(self.record_audio)

        self.stop_record_button = QPushButton("Stop", self)
        self.stop_record_button.setMaximumHeight(30)
        self.stop_record_button.setVisible(False)
        self.stop_record_button.clicked.connect(self.stop_record)

        self.text_display = QTextEdit(self)
        self.text_display.setReadOnly(True)
        self.text_display.setMaximumHeight(50)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.sign_language_label)
        main_layout.addWidget(self.recording_label)
        main_layout.addWidget(self.record_button)
        main_layout.addWidget(self.stop_record_button)
        main_layout.addWidget(self.text_display)
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.recording_thread = AudioRecorder()
        self.recording_thread.signal.connect(self._recorded_audio_thread)

    def record_audio(self):
        self.text_display.clear()
        self.recording_label.setVisible(True)
        self.record_button.setVisible(False)
        self.stop_record_button.setVisible(True)
        self.stop_record_button.setEnabled(True)
        self.recording_thread.recording = True
        self.recording_thread.start()

    def stop_record(self):
        self.stop_record_button.setEnabled(False)
        self.recording_thread.stop_recording()
        loop = QEventLoop()
        QTimer.singleShot(3000, loop.quit)
        loop.exec_()
        self.recording_label.setVisible(False)
        self.stop_record_button.setVisible(False)
        self.record_button.setVisible(True)
        

    def _recorded_audio_thread(self, recognized_text):
        if isinstance(recognized_text, str):  # Kiểm tra xem recognized_text có phải là chuỗi không
            self.text_display.setPlainText(recognized_text)
            self.display_sign_language_image(recognized_text)
        else:
            print("Error: recognized_text is not a string")

    def display_sign_language_image(self, word):
        image_path = os.path.join("sign_language_images", word.lower() + ".jpg")
        if os.path.exists(image_path):
            image = cv2.imread(image_path)
            if image is not None:
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                h, w, ch = image_rgb.shape
                bytesPerLine = ch * w
                qImg = QImage(image_rgb.data, w, h, bytesPerLine, QImage.Format_RGB888)
                qImg = qImg.scaled(200, 200, Qt.KeepAspectRatio)
                self.sign_language_label.setPixmap(QPixmap.fromImage(qImg))
        else:
            print("Sign language image not found for word:", word)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = YOLO_GUI()
    mainWindow.show()
    sys.exit(app.exec_())
