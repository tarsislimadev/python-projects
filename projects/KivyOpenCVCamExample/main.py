import cv2
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.label import Label


class CameraWidget(Image):
    def __init__(self, **kwargs):
        super(CameraWidget, self).__init__(**kwargs)
        self.capture = None
        self.fps = 30
        self.current_filter = 'none'
        self.camera_available = False

    def start_camera(self):
        if self.capture is None:
            self.capture = cv2.VideoCapture(0)
            if not self.capture.isOpened():
                print("Error: Could not open camera")
                self.camera_available = False
                return
            self.camera_available = True
        Clock.schedule_interval(self.update_frame, 1.0 / self.fps)

    def stop_camera(self):
        Clock.unschedule(self.update_frame)

    def update_frame(self, dt):
        if not self.camera_available or self.capture is None:
            return
        ret, frame = self.capture.read()
        if ret:
            processed_frame = self.apply_filter(frame)

            frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            frame_flipped = cv2.flip(frame_rgb, 0)

            buf = frame_flipped.tostring()
            image_texture = Texture.create(size=(frame_rgb.shape[1], frame_rgb.shape[0]), colorfmt='rgb')
            image_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

            self.texture = image_texture

    def apply_filter(self, frame):
        if self.current_filter == 'none':
            return frame
        elif self.current_filter == 'gray':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        elif self.current_filter == 'blur':
            return cv2.GaussianBlur(frame, (15, 15), 0)
        elif self.current_filter == 'edge':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        elif self.current_filter == 'sharpen':
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            return cv2.filter2D(frame, -1, kernel)
        elif self.current_filter == 'emboss':
            kernel = np.array([[-2,-1,0], [-1,1,1], [0,1,2]])
            return cv2.filter2D(frame, -1, kernel)
        elif self.current_filter == 'sepia':
            sepia_filter = np.array([[0.272, 0.534, 0.131],
                                   [0.349, 0.686, 0.168],
                                   [0.393, 0.769, 0.189]])
            sepia_img = frame.dot(sepia_filter.T)
            sepia_img = np.clip(sepia_img, 0, 255)
            return sepia_img.astype(np.uint8)
        elif self.current_filter == 'invert':
            return cv2.bitwise_not(frame)
        elif self.current_filter == 'hsv_threshold':
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_blue = np.array([100, 50, 50])
            upper_blue = np.array([130, 255, 255])
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            result = cv2.bitwise_and(frame, frame, mask=mask)
            return result
        return frame

    def set_filter(self, filter_name):
        self.current_filter = filter_name

    def release_camera(self):
        if self.capture is not None:
            self.capture.release()


class CameraApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        title_label = Label(text='Real-Time Camera Processing with Kivy & OpenCV',
                           size_hint=(1, 0.1),
                           font_size='20sp')
        main_layout.add_widget(title_label)

        content_layout = BoxLayout(orientation='horizontal', spacing=10)

        self.camera_widget = CameraWidget(size_hint=(0.7, 1))
        content_layout.add_widget(self.camera_widget)

        controls_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1), spacing=10)

        start_btn = Button(text='Start Camera', size_hint=(1, 0.1))
        start_btn.bind(on_press=self.start_camera)
        controls_layout.add_widget(start_btn)

        stop_btn = Button(text='Stop Camera', size_hint=(1, 0.1))
        stop_btn.bind(on_press=self.stop_camera)
        controls_layout.add_widget(stop_btn)

        filters_label = Label(text='Filters:', size_hint=(1, 0.08), font_size='16sp')
        controls_layout.add_widget(filters_label)

        filters = [
            ('None', 'none'),
            ('Grayscale', 'gray'),
            ('Blur', 'blur'),
            ('Edge Detection', 'edge'),
            ('Sharpen', 'sharpen'),
            ('Emboss', 'emboss'),
            ('Sepia', 'sepia'),
            ('Invert', 'invert'),
            ('Blue HSV', 'hsv_threshold')
        ]

        for filter_name, filter_code in filters:
            btn = Button(text=filter_name, size_hint=(1, 0.08))
            btn.bind(on_press=lambda x, code=filter_code: self.set_filter(code))
            controls_layout.add_widget(btn)

        content_layout.add_widget(controls_layout)
        main_layout.add_widget(content_layout)

        return main_layout

    def start_camera(self, instance):
        self.camera_widget.start_camera()

    def stop_camera(self, instance):
        self.camera_widget.stop_camera()

    def set_filter(self, filter_code):
        self.camera_widget.set_filter(filter_code)

    def on_stop(self):
        self.camera_widget.release_camera()


if __name__ == '__main__':
    CameraApp().run()