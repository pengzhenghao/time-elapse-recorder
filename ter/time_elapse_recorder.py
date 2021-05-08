"""
by PENG Zhenghao
"""
import time

import cv2

from ter.utils import ImageEncoder, get_time_str, ForceFPS, get_window_close


def put_text(frame, text, y, x=8):
    cv2.putText(
        frame, text, org=(x, y), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.5,
        color=(255, 255, 255), thickness=1, lineType=cv2.LINE_AA
    )


class DisplayThread:
    def __init__(self, width, height, output_fps, window_name, display_size=256):
        if width > height:
            self.show_width = display_size
            self.show_height = int(display_size / width * height)
        else:
            self.show_height = display_size
            self.show_width = int(display_size / height * width)
        self.start_time = time.time()
        self.output_fps = output_fps
        self.window_name = window_name
        cv2.namedWindow(self.window_name, cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_AUTOSIZE)

    def display(self, raw_frame, frame_count):
        frame = cv2.resize(raw_frame, (self.show_width, self.show_height), interpolation=cv2.INTER_NEAREST)
        text = 'Recording...'
        put_text(frame, text, 115)
        text = "Press Q/ESC to exit."
        put_text(frame, text, 130)
        text = 'Frames recorded: {}'.format(frame_count)
        put_text(frame, text, 25)
        text = 'Elapsed: {:.1f}s'.format(time.time() - self.start_time)
        put_text(frame, text, 40)
        text = 'Video length: {:.2f}s'.format((frame_count) / self.output_fps)
        put_text(frame, text, 55)
        cv2.imshow(self.window_name, frame)

    def close(self):
        cv2.destroyAllWindows()


class RecordThread:
    def __init__(self, file_name, width, height, output_fps):
        self.encoder = ImageEncoder(file_name, (height, width, 3), output_fps)
        self.frame_count = 0

    def record(self, frame):
        if self.frame_count > 1:
            self.encoder.capture_frame(frame)
        self.frame_count += 1

    def close(self):
        self.encoder.close()

    def get_frame_count(self):
        return self.frame_count


class TimeElapseRecorder:
    def __init__(self, interval=1, output_fps=30, display_fps=5):
        # Setup camera
        cap = cv2.VideoCapture(0)  # Capture video from camera
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        cap.set(cv2.CAP_PROP_FPS, display_fps)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
        self.cap = cap
        self.window_name = "Time-elapse Recorder"
        self.display_thread = DisplayThread(
            width=width, height=height, output_fps=output_fps, window_name=self.window_name
        )
        self.file_name = 'video_{}.mp4'.format(get_time_str())
        self.output_fps = output_fps
        self.interval = interval
        self.record_thread = RecordThread(
            width=width, height=height, output_fps=output_fps, file_name=self.file_name
        )
        assert 1 / display_fps < interval, "Please make sure the interval is greater than {}".format(1 / display_fps)
        self.force_fps = ForceFPS(interval=interval, display_fps=display_fps)

    def run(self):
        try:
            while self.cap.isOpened():
                should_record, should_display = self.force_fps.tick()
                ret, frame = self.cap.read()
                if ret:
                    if should_record:
                        self.record_thread.record(frame)
                    if should_display:
                        self.display_thread.display(frame, self.record_thread.get_frame_count())
                else:
                    break
                if get_window_close(window_name=self.window_name):  # Hit 'q' or 'esc' to exit
                    print("Received stop command from user!")
                    break
        except KeyboardInterrupt:
            print("Received stop command from user!")

    def __del__(self):
        self.close()

    def close(self):
        print("Processing video! Please wait for a while!")
        self.display_thread.close()
        self.record_thread.close()
        self.cap.release()
        frame_count = self.record_thread.get_frame_count()
        print(
            "Program successfully exited! We have recorded {} frames, namely {} seconds! "
            "The output video would have length: {:.2f} seconds! "
            "The file is saved at: {}".format(
                frame_count, frame_count * self.interval, frame_count / self.output_fps, self.file_name
            )
        )


if __name__ == '__main__':
    # Test use only
    ter = TimeElapseRecorder()
    ter.run()
    ter.close()
