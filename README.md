# Video Kaleidoscope

Video Kaleidoscope is a video manipulation tool built using Python, OpenCV, and Tkinter. It allows users to load a video file and apply various visual effects in real time, such as flipping, rotating, zooming, panning, mirroring, and applying color maps (LUTs). The interface includes intuitive buttons for playback control, frame stepping, snapshot capture, and various video transformations. It's designed for both interactive exploration and creative manipulation of video content, providing a kaleidoscopic viewing experience.

## Requirements

The following Python modules are required for this application:
- opencv-python
- numpy
- Pillow

You can install these modules using pip:
```sh
pip install opencv-python numpy Pillow
```

## Usage

To run the application, use the following command:
```sh
python video_kaleidoscope.py <video_path>
```
Replace `<video_path>` with the path to the video file you want to use.

## Controls

The application provides the following commands and buttons:
- **Play/Pause**: Button to toggle between play and pause.
- **Stop**: Button to stop the video.
- **Flip Horizontal**: Button to flip the video horizontally.
- **Flip Vertical**: Button to flip the video vertically.
- **Snapshot**: Button to take a snapshot of the current frame.
- **Mirror Left**: Button to cycle through mirror levels (center, thirds, quarters) on the left side.
- **Mirror Right**: Button to cycle through mirror levels (center, thirds, quarters) on the right side.
- **Rotate Left 10°**: Button to rotate the video left by 10 degrees.
- **Rotate Right 10°**: Button to rotate the video right by 10 degrees.
- **Zoom In**: Button to zoom in.
- **Zoom Out**: Button to zoom out.
- **Frame Forward**: Button to move forward one frame.
- **Frame Reverse**: Button to move backward one frame.
- **Pan Up**: Button to pan up when zoomed in.
- **Pan Down**: Button to pan down when zoomed in.
- **Pan Left**: Button to pan left when zoomed in.
- **Pan Right**: Button to pan right when zoomed in.
- **Center Pan**: Button to recenter the panning position.
- **LUT Selection**: Dropdown to apply a color map (LUT) to the video.
- **Rotation Slider**: Slider to adjust the rotation angle.
- **Zoom Slider**: Slider to adjust the zoom level.

