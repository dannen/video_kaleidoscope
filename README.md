# Video Kaleidoscope

Video Kaleidoscope is a video manipulation tool built using Python, OpenCV, and Tkinter. It allows users to load a video file and apply various visual effects in real time, such as flipping, rotating, zooming, panning, mirroring, kaleidoscope effects, and applying color maps (LUTs). The interface includes intuitive buttons for playback control, frame stepping, snapshot capture, and various video transformations. It's designed for both interactive exploration and creative manipulation of video content, providing a kaleidoscopic viewing experience.

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

- **Reset**: Button to reset all applied effects and return the video to its original state. [![Reset Button](icons/reset_button.png)](icons/reset_button.png)
- **Play/Pause**: Button to toggle between play and pause. [![Play Button](icons/play_button.png)](icons/play_button.png) [![Pause Button](icons/pause_button.png)](icons/pause_button.png)
- **Stop**: Button to stop the video. [![Stop Button](icons/stop_button.png)](icons/stop_button.png)
- **Flip Horizontal**: Button to flip the video horizontally. [![Flip Horizontal](icons/flip_horizontal.png)](icons/flip_horizontal.png)
- **Flip Vertical**: Button to flip the video vertically. [![Flip Vertical](icons/flip_vertical.png)](icons/flip_vertical.png)
- **Mirror Up**: Button to mirror the top half to the bottom. [![Mirror Up](icons/mirror_up.png)](icons/mirror_up.png)
- **Mirror Down**: Button to mirror the bottom half to the top. [![Mirror Down](icons/mirror_down.png)](icons/mirror_down.png)
- **Snapshot**: Button to take a snapshot of the current frame. [![Snapshot Button](icons/snapshot_button.png)](icons/snapshot_button.png)
- **Mirror Left**: Button to cycle through mirror levels (center, thirds, quarters) on the left side. [![Mirror Left](icons/mirror_left.png)](icons/mirror_left.png)
- **Mirror Right**: Button to cycle through mirror levels (center, thirds, quarters) on the right side. [![Mirror Right](icons/mirror_right.png)](icons/mirror_right.png)
- **Zoom In**: Button to zoom in. [![Zoom In](icons/zoom_in.png)](icons/zoom_in.png)
- **Zoom Out**: Button to zoom out. [![Zoom Out](icons/zoom_out.png)](icons/zoom_out.png)
- **Frame Forward**: Button to move forward one frame. [![Frame Forward](icons/frame_forward.png)](icons/frame_forward.png)
- **Frame Reverse**: Button to move backward one frame. [![Frame Reverse](icons/frame_reverse.png)](icons/frame_reverse.png)
- **Faster**: Button to increase playback speed. [![Faster](icons/faster.png)](icons/faster.png)
- **Slower**: Button to decrease playback speed. [![Slower](icons/slower.png)](icons/slower.png)
- **Pan Up**: Button to pan up when zoomed in. [![Pan Up](icons/pan_up.png)](icons/pan_up.png)
- **Pan Down**: Button to pan down when zoomed in. [![Pan Down](icons/pan_down.png)](icons/pan_down.png)
- **Pan Left**: Button to pan left when zoomed in. [![Pan Left](icons/pan_left.png)](icons/pan_left.png)
- **Pan Right**: Button to pan right when zoomed in. [![Pan Right](icons/pan_right.png)](icons/pan_right.png)
- **Center Pan**: Button to recenter the panning position. [![Center Pan](icons/pan_center.png)](icons/pan_center.png)
- **Reverse Playback**: Button to increase reverse playback speed (up to 8x). [![Reverse Playback](icons/reverse_playback.png)](icons/reverse_playback.png)
- **LUT Selection**: Dropdown to apply a color map (LUT) to the video.
- **Rotation Slider**: Slider to adjust the rotation angle.
- **Zoom Slider**: Slider to adjust the zoom level.
- **Brightness Slider**: Slider to adjust the brightness level.
- **Kaleidoscope Segments Slider**: Slider to adjust the number of kaleidoscope segments.
- **Mirror Nine**: Button to apply a nine-part mirror effect.
- **Mirror Six**: Button to apply a six-part mirror effect in 60-degree increments.
- **Mirror Three**: Button to apply a three-part mirror effect in 120-degree increments.

These controls enable a wide range of video transformations, allowing users to explore and manipulate video content creatively.

