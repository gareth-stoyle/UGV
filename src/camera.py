from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from typing import Tuple


class Camera:
    """
    A simple class to initialize and operate the camera using the picamera2 library.

    Attributes:
        resolution (Tuple[int, int]): The resolution of the camera in (width, height).
        flip (bool): Whether to apply flipping to the camera feed.
    """

    def __init__(self, resolution: Tuple[int, int] = (1280, 720), flip: bool = True):
        """
        Initializes the camera with the specified resolution and flipping options.

        Args:
            resolution (Tuple[int, int]): Desired resolution as (width, height).
            flip (bool): Set to True to enable horizontal and vertical flipping.
        """
        self.camera = Picamera2()
        self.encoder = H264Encoder()
        config: dict = self.camera.create_video_configuration(main={"size": resolution})
        self.camera.configure(config)
        if flip:
            self.camera.set_controls({"FlipHorizontal": True, "FlipVertical": True})
        self.camera.start()

    def start_recording(self, path: str, video_file: str) -> None:
        """
        Starts recording a video to the specified path.

        Args:
            path (str): The directory where the video file will be saved.
            video_file (str): The name of the video file (e.g., 'video.h264').
        """
        output: str = f"{path}/{video_file}"
        file_output = FfmpegOutput(output, audio=False)
        self.camera.start_recording(self.encoder, file_output)

    def stop_recording(self) -> None:
        """
        Stops the ongoing video recording.
        """
        self.camera.stop_recording()


if __name__ == "__main__":
    camera = Camera(resolution=(1920, 1080), flip=False)
    camera.start_recording("/home/gareth/ugv_rpi", "example_video.mp4")

    # Let the camera record for 5 seconds
    import time

    time.sleep(5)

    camera.stop_recording()
