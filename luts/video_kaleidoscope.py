# Requires: pip install opencv-python numpy Pillow
import sys
from datetime import datetime
import tkinter as tk
from tkinter import Scale, HORIZONTAL, OptionMenu, StringVar
import cv2
import numpy as np
from PIL import Image, ImageTk

LUTS = {
    'WHITEHOT': cv2.COLORMAP_BONE,
    'BLACKHOT': cv2.COLORMAP_JET,
    'REDHOT': cv2.COLORMAP_HOT,
    'RAINBOW': cv2.COLORMAP_RAINBOW,
    'OCEAN': cv2.COLORMAP_OCEAN,
    'LAVA': cv2.COLORMAP_PINK,
    'ARCTIC': cv2.COLORMAP_WINTER,
    'GLOBOW': cv2.COLORMAP_PARULA,
    'GRADEDFIRE': cv2.COLORMAP_AUTUMN,
    'INSTALERT': cv2.COLORMAP_SUMMER,
    'SPRING': cv2.COLORMAP_SPRING,
    'SUMMER': cv2.COLORMAP_SUMMER,
    'COOL': cv2.COLORMAP_COOL,
    'HSV': cv2.COLORMAP_HSV,
    'PINK': cv2.COLORMAP_PINK,
    'HOT': cv2.COLORMAP_HOT,
    'MAGMA': cv2.COLORMAP_MAGMA,
    'INFERNO': cv2.COLORMAP_INFERNO,
    'PLASMA': cv2.COLORMAP_PLASMA,
    'VIRIDIS': cv2.COLORMAP_VIRIDIS,
    'CIVIDIS': cv2.COLORMAP_CIVIDIS,
    'ISOTHERM_RED': lambda: create_custom_lut('red', 64),
    'ISOTHERM_GREEN': lambda: create_custom_lut('green', 64),
    'ISOTHERM_BLUE': lambda: create_custom_lut('blue', 64)
}


def create_custom_lut(color, color_gradient_step):
    """Creates a custom LUT using predefined color data."""
    if color_gradient_step <= 0:
        raise ValueError("color_gradient_step must be greater than 0.")

    if color == 'red':
        gradient_colors = ((0, 0, 64), (0, 0, 255), color_gradient_step)
    elif color == 'green':
        gradient_colors = ((0, 64, 0), (0, 255, 0), color_gradient_step)
    elif color == 'blue':
        gradient_colors = ((64, 0, 0), (255, 0, 0), color_gradient_step)
    else:
        raise ValueError(
            "Unsupported color for LUT creation. Supported colors are 'red', 'green', and 'blue'.")

    black_to_white_step = 256 - color_gradient_step
    black_to_white = np.linspace(
        (0, 0, 0), (255, 255, 255), black_to_white_step).astype(np.uint8)
    color_gradient = np.linspace(*gradient_colors).astype(np.uint8)
    custom_colors = np.concatenate((black_to_white, color_gradient))

    # Ensure we have exactly 256 colors by interpolating if necessary
    if len(custom_colors) != 256:
        custom_colors = np.linspace(
            custom_colors[0], custom_colors[-1], 256, dtype=np.uint8)

    # Create a custom LUT with 256 entries
    custom_lut = custom_colors.reshape((256, 1, 3))
    return custom_lut


class VideoAttributes:
    def __init__(self):
        self.mirror_left_level = 0
        self.mirror_right_level = 0
        self.flip_horizontal = False
        self.flip_vertical = False
        self.flip_up_down = False
        self.rotation_angle = 0
        self.playback_speed = 1.0
        self.reverse_playback_speed = 1.0
        self.zoom_factor = 1.0
        self.paused = False
        self.pan_x = 0
        self.pan_y = 0
        self.kaleidoscope_segments = 0  # Set to 0 by default


class VideoKaleidoscope:
    def __init__(self, input_video_path):
        self.video_path = input_video_path
        self.cap = cv2.VideoCapture(input_video_path)
        if not self.cap.isOpened():
            print(f"Error: Unable to open video file {input_video_path}")
            sys.exit(1)
        self.attributes = VideoAttributes()
        self.current_frame = None
        self.video_stopped = False
        self.lut = None
        self.root = tk.Tk()
        self.root.title("Video Kaleidoscope")

        # Set up video display area
        self.video_label = tk.Label(self.root)
        self.video_label.pack()

        # Set up controls
        self.create_controls()

        # Start updating video
        self.update_video()

        self.root.mainloop()

    def create_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack()

        # Load control icons (25x25 pixels) with error handling
        try:
            play_icon = ImageTk.PhotoImage(Image.open(
                "icons/play_button.png").resize((25, 25)))
            pause_icon = ImageTk.PhotoImage(Image.open(
                "icons/pause_button.png").resize((25, 25)))
            stop_icon = ImageTk.PhotoImage(Image.open(
                "icons/stop_button.png").resize((25, 25)))
            flip_horizontal_icon = ImageTk.PhotoImage(
                Image.open("icons/flip_horizontal.png").resize((25, 25)))
            flip_vertical_icon = ImageTk.PhotoImage(
                Image.open("icons/flip_vertical.png").resize((25, 25)))
            flip_up_down_icon = ImageTk.PhotoImage(
                Image.open("icons/flip_up_down.png").resize((25, 25)))
            snapshot_icon = ImageTk.PhotoImage(Image.open(
                "icons/snapshot_button.png").resize((25, 25)))
            mirror_left_icon = ImageTk.PhotoImage(
                Image.open("icons/mirror_left.png").resize((25, 25)))
            mirror_right_icon = ImageTk.PhotoImage(
                Image.open("icons/mirror_right.png").resize((25, 25)))
            exit_icon = ImageTk.PhotoImage(Image.open(
                "icons/exit_button.png").resize((25, 25)))
            zoom_in_icon = ImageTk.PhotoImage(
                Image.open("icons/zoom_in.png").resize((25, 25)))
            zoom_out_icon = ImageTk.PhotoImage(
                Image.open("icons/zoom_out.png").resize((25, 25)))
            frame_forward_icon = ImageTk.PhotoImage(
                Image.open("icons/frame_forward.png").resize((25, 25)))
            frame_reverse_icon = ImageTk.PhotoImage(
                Image.open("icons/frame_reverse.png").resize((25, 25)))
            faster_icon = ImageTk.PhotoImage(
                Image.open("icons/faster.png").resize((25, 25)))
            slower_icon = ImageTk.PhotoImage(
                Image.open("icons/slower.png").resize((25, 25)))
            pan_up_icon = ImageTk.PhotoImage(
                Image.open("icons/pan_up.png").resize((25, 25)))
            pan_down_icon = ImageTk.PhotoImage(
                Image.open("icons/pan_down.png").resize((25, 25)))
            pan_left_icon = ImageTk.PhotoImage(
                Image.open("icons/pan_left.png").resize((25, 25)))
            pan_right_icon = ImageTk.PhotoImage(
                Image.open("icons/pan_right.png").resize((25, 25)))
            pan_center_icon = ImageTk.PhotoImage(
                Image.open("icons/pan_center.png").resize((25, 25)))
            reverse_playback_icon = ImageTk.PhotoImage(
                Image.open("icons/reverse_playback.png").resize((25, 25)))
        except FileNotFoundError as e:
            print(f"Error: {e}")
            sys.exit(1)

        # Buttons for controls with icons
        controls = [
            (play_icon, self.toggle_pause),
            (pause_icon, self.toggle_pause),
            (stop_icon, self.stop_video),
            (flip_horizontal_icon, self.toggle_flip_horizontal),
            (flip_vertical_icon, self.toggle_flip_vertical),
            (flip_up_down_icon, self.toggle_flip_up_down),
            (snapshot_icon, self.snapshot),
            (mirror_left_icon, lambda: self.toggle_mirror_level('left')),
            (mirror_right_icon, lambda: self.toggle_mirror_level('right')),
            (zoom_in_icon, lambda: self.set_zoom_factor(
                self.attributes.zoom_factor + 0.1)),
            (zoom_out_icon, lambda: self.set_zoom_factor(
                self.attributes.zoom_factor - 0.1)),
            (frame_forward_icon, self.frame_forward),
            (frame_reverse_icon, self.frame_reverse),
            (faster_icon, lambda: self.set_playback_speed(
                self.attributes.playback_speed * 2)),
            (slower_icon, lambda: self.set_playback_speed(
                self.attributes.playback_speed / 2)),
            (pan_up_icon, lambda: self.pan_video(0, -10)),
            (pan_down_icon, lambda: self.pan_video(0, 10)),
            (pan_left_icon, lambda: self.pan_video(-10, 0)),
            (pan_right_icon, lambda: self.pan_video(10, 0)),
            (pan_center_icon, self.center_pan),
            (reverse_playback_icon, self.toggle_reverse_playback_speed),
            (exit_icon, self.exit_program)
        ]
        for idx, (icon, command) in enumerate(controls):
            tk.Button(control_frame, image=icon, command=command).grid(
                row=idx // 8, column=idx % 8)

        # LUT selection dropdown
        self.lut_var = StringVar(self.root)
        self.lut_var.set("None")  # Default value
        luts = ["None"] + list(LUTS.keys())
        lut_menu = OptionMenu(control_frame, self.lut_var,
                              *luts, command=self.set_lut)
        lut_menu.grid(row=3, column=0, columnspan=2)

        # Keep references to the images to prevent garbage collection
        self.icons = [icon for icon, _ in controls]

        # Sliders for rotation, zoom, playback speed, and kaleidoscope segments
        sliders = [
            ("Rotation", 0, 359, HORIZONTAL, lambda x: self.set_rotation_angle(
                int(x) - self.attributes.rotation_angle)),
            ("Zoom", 1, 50, HORIZONTAL, lambda x: self.set_zoom_factor(float(x) / 10)),
            ("Playback Speed", 0.1, 4.0, HORIZONTAL,
             lambda x: self.set_playback_speed(float(x))),
            ("Kaleidoscope Segments", 0, 12, HORIZONTAL,
             lambda x: self.set_kaleidoscope_segments(int(x)))
        ]
        for idx, (label, frm, to, orient, command) in enumerate(sliders):
            Scale(control_frame, from_=frm, to=to, orient=orient, label=label,
                  command=command).grid(row=3 + idx, column=2, columnspan=4)

    def set_kaleidoscope_segments(self, segments):
        self.attributes.kaleidoscope_segments = segments
        if self.attributes.paused:
            self.apply_effects()

    def toggle_pause(self):
        if self.video_stopped:
            self.cap = cv2.VideoCapture(self.video_path)
            if not self.cap.isOpened():
                print(f"Error: Unable to reopen video file {self.video_path}")
                return
            self.video_stopped = False
            self.attributes.paused = False
        else:
            self.attributes.paused = not self.attributes.paused

        if self.attributes.paused and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame
                self.apply_effects()

    def stop_video(self):
        self.cap.release()
        self.video_label.configure(image='')
        self.video_stopped = True

    def toggle_mirror_level(self, side):
        if side == 'left':
            self.attributes.mirror_left_level = (
                self.attributes.mirror_left_level + 1) % 4
        elif side == 'right':
            self.attributes.mirror_right_level = (
                self.attributes.mirror_right_level + 1) % 4
        if self.attributes.paused:
            self.apply_effects()

    def toggle_flip_horizontal(self):
        self.attributes.flip_horizontal = not self.attributes.flip_horizontal
        if self.attributes.paused:
            self.apply_effects()

    def toggle_flip_vertical(self):
        self.attributes.flip_vertical = not self.attributes.flip_vertical
        if self.attributes.paused:
            self.apply_effects()

    def toggle_flip_up_down(self):
        self.attributes.flip_up_down = not self.attributes.flip_up_down
        if self.attributes.paused:
            self.apply_effects()

    def set_rotation_angle(self, angle):
        self.attributes.rotation_angle = (
            self.attributes.rotation_angle + angle) % 360
        if self.attributes.paused:
            self.apply_effects()

    def set_playback_speed(self, speed):
        self.attributes.playback_speed = max(0.05, min(speed, 16.0))

    def set_zoom_factor(self, zoom):
        self.attributes.zoom_factor = max(1.0, zoom)
        if self.attributes.paused:
            self.apply_effects()

    def pan_video(self, delta_x, delta_y):
        if self.attributes.zoom_factor > 1.0:
            self.attributes.pan_x += delta_x
            self.attributes.pan_y += delta_y
            if self.attributes.paused:
                self.apply_effects()

    def center_pan(self):
        self.attributes.pan_x = 0
        self.attributes.pan_y = 0
        if self.attributes.paused:
            self.apply_effects()

    def set_lut(self, lut_name):
        if lut_name == "None":
            self.lut = None
        else:
            lut_function = LUTS.get(lut_name)
            if lut_function is None:
                print(f"Error: LUT '{lut_name}' not found.")
                return
            self.lut = lut_function() if callable(lut_function) else lut_function
        if self.attributes.paused:
            self.apply_effects()

    def apply_lut(self, frame):
        if self.lut is not None:
            if isinstance(self.lut, np.ndarray):
                frame = cv2.LUT(frame, self.lut)
            else:
                frame = cv2.applyColorMap(frame, self.lut)
        return frame

    def snapshot(self):
        if self.current_frame is not None:
            frame = self.current_frame.copy()
            height, width = frame.shape[:2]

            # Apply zoom and pan
            center_x, center_y = width // 2 + \
                self.attributes.pan_x, height // 2 + self.attributes.pan_y
            new_width, new_height = int(
                width / self.attributes.zoom_factor), int(height / self.attributes.zoom_factor)
            x1, y1 = max(0, center_x - new_width // 2), max(0,
                                                            center_y - new_height // 2)
            x2, y2 = min(width, center_x + new_width //
                         2), min(height, center_y + new_height // 2)
            frame = frame[y1:y2, x1:x2]
            frame = cv2.resize(frame, (width, height))

            # Apply rotation
            if self.attributes.rotation_angle != 0:
                matrix = cv2.getRotationMatrix2D(
                    (width // 2, height // 2), self.attributes.rotation_angle, 1)
                frame = cv2.warpAffine(
                    frame, matrix, (width, height), borderMode=cv2.BORDER_REFLECT)

            # Apply flip
            if self.attributes.flip_horizontal:
                frame = cv2.flip(frame, 1)
            if self.attributes.flip_vertical:
                frame = cv2.flip(frame, 0)
            if self.attributes.flip_up_down:
                frame = cv2.flip(frame, 0)

            # Apply mirror effects for the left side
            if self.attributes.mirror_left_level == 1:
                left_half = frame[:, :width // 2]
                frame[:, width // 2:] = cv2.flip(left_half, 1)
            elif self.attributes.mirror_left_level == 2:
                third_width = width // 3
                left = frame[:, :third_width]
                right = frame[:, 2 * third_width:]
                min_width = min(left.shape[1], right.shape[1])
                frame[:, third_width:third_width +
                      min_width] = cv2.flip(left[:, :min_width], 1)
                frame[:, :min_width] = cv2.flip(right[:, :min_width], 1)
            elif self.attributes.mirror_left_level == 3:
                quarter_width = width // 4
                for i in range(4):
                    if i % 2 == 0:
                        frame[:, i * quarter_width:(i + 1) * quarter_width] = cv2.flip(
                            frame[:, i * quarter_width:(i + 1) * quarter_width], 1)

            # Apply mirror effects for the right side
            if self.attributes.mirror_right_level == 1:
                right_half = frame[:, width // 2:]
                frame[:, :width // 2] = cv2.flip(right_half, 1)
            elif self.attributes.mirror_right_level == 2:
                third_width = width // 3
                left = frame[:, :third_width]
                right = frame[:, 2 * third_width:]
                min_width = min(left.shape[1], right.shape[1])
                frame[:, third_width:third_width +
                      min_width] = cv2.flip(right[:, :min_width], 1)
                frame[:, 2 * third_width:2 * third_width +
                      min_width] = cv2.flip(left[:, :min_width], 1)
            elif self.attributes.mirror_right_level == 3:
                quarter_width = width // 4
                for i in range(4):
                    if i % 2 == 1:
                        frame[:, i * quarter_width:(i + 1) * quarter_width] = cv2.flip(
                            frame[:, i * quarter_width:(i + 1) * quarter_width], 1)

            # Apply LUT
            frame = self.apply_lut(frame)

            # Save the processed frame as an image file
            timestamp = datetime.now().strftime('%Y%m%d%M%S')
            filename = f'snapshot-{timestamp}.png'
            cv2.imwrite(filename, frame)
            print(f'Snapshot saved as {filename}')

    def frame_forward(self):
        if self.cap.isOpened():
            self.attributes.paused = True
            self.cap.set(cv2.CAP_PROP_POS_FRAMES,
                         self.cap.get(cv2.CAP_PROP_POS_FRAMES) + 1)
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame
                self.apply_effects()

    def frame_reverse(self):
        if self.cap.isOpened():
            self.attributes.paused = True
            current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, current_frame - 2))
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame
                self.apply_effects()

    def toggle_reverse_playback_speed(self):
        self.attributes.reverse_playback_speed *= 2
        if self.attributes.reverse_playback_speed > 8.0:
            self.attributes.reverse_playback_speed = 1.0

    def apply_effects(self):
        if self.current_frame is not None:
            frame = self.current_frame.copy()
            height, width = frame.shape[:2]

            # Apply zoom and pan
            center_x, center_y = width // 2 + \
                self.attributes.pan_x, height // 2 + self.attributes.pan_y
            new_width, new_height = int(
                width / self.attributes.zoom_factor), int(height / self.attributes.zoom_factor)
            x1, y1 = max(0, center_x - new_width // 2), max(0,
                                                            center_y - new_height // 2)
            x2, y2 = min(width, center_x + new_width //
                         2), min(height, center_y + new_height // 2)
            frame = frame[y1:y2, x1:x2]
            frame = cv2.resize(frame, (width, height))

            # Apply rotation
            if self.attributes.rotation_angle != 0:
                matrix = cv2.getRotationMatrix2D(
                    (width // 2, height // 2), self.attributes.rotation_angle, 1)
                frame = cv2.warpAffine(
                    frame, matrix, (width, height), borderMode=cv2.BORDER_REFLECT)

            # Apply flip
            if self.attributes.flip_horizontal:
                frame = cv2.flip(frame, 1)
            if self.attributes.flip_vertical:
                frame = cv2.flip(frame, 0)
            if self.attributes.flip_up_down:
                frame = cv2.flip(frame, 0)

            # Apply mirror effects for the left side
            if self.attributes.mirror_left_level == 1:
                left_half = frame[:, :width // 2]
                frame[:, width // 2:] = cv2.flip(left_half, 1)
            elif self.attributes.mirror_left_level == 2:
                third_width = width // 3
                left = frame[:, :third_width]
                right = frame[:, 2 * third_width:]
                min_width = min(left.shape[1], right.shape[1])
                frame[:, third_width:third_width +
                      min_width] = cv2.flip(left[:, :min_width], 1)
                frame[:, :min_width] = cv2.flip(right[:, :min_width], 1)
            elif self.attributes.mirror_left_level == 3:
                quarter_width = width // 4
                for i in range(4):
                    if i % 2 == 0:
                        frame[:, i * quarter_width:(i + 1) * quarter_width] = cv2.flip(
                            frame[:, i * quarter_width:(i + 1) * quarter_width], 1)

            # Apply mirror effects for the right side
            if self.attributes.mirror_right_level == 1:
                right_half = frame[:, width // 2:]
                frame[:, :width // 2] = cv2.flip(right_half, 1)
            elif self.attributes.mirror_right_level == 2:
                third_width = width // 3
                left = frame[:, :third_width]
                right = frame[:, 2 * third_width:]
                min_width = min(left.shape[1], right.shape[1])
                frame[:, third_width:third_width +
                      min_width] = cv2.flip(right[:, :min_width], 1)
                frame[:, 2 * third_width:2 * third_width +
                      min_width] = cv2.flip(left[:, :min_width], 1)
            elif self.attributes.mirror_right_level == 3:
                quarter_width = width // 4
                for i in range(4):
                    if i % 2 == 1:
                        frame[:, i * quarter_width:(i + 1) * quarter_width] = cv2.flip(
                            frame[:, i * quarter_width:(i + 1) * quarter_width], 1)

            # Apply kaleidoscope effect if enabled
            if self.attributes.kaleidoscope_segments > 0:
                frame = self.kaleidoscope_effect(frame)

            # Apply LUT
            frame = self.apply_lut(frame)

            # Convert frame to ImageTk format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)

            # Update video label
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

    def kaleidoscope_effect(self, frame):
        height, width = frame.shape[:2]
        center_x, center_y = width // 2, height // 2
        mask = np.zeros_like(frame)

        angle_step = 360 // self.attributes.kaleidoscope_segments
        for i in range(self.attributes.kaleidoscope_segments):
            angle = i * angle_step
            matrix = cv2.getRotationMatrix2D((center_x, center_y), angle, 1)
            rotated = cv2.warpAffine(frame, matrix, (width, height))
            mask = cv2.add(mask, rotated)

        return mask

    def update_video(self):
        if self.cap.isOpened() and not self.attributes.paused:
            if self.attributes.reverse_playback_speed > 1.0:
                current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                new_frame = max(0, current_frame -
                                self.attributes.reverse_playback_speed)
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame
                self.apply_effects()

        # Schedule the next update
        self.root.after(
            int(1000 / (30 * self.attributes.playback_speed)), self.update_video)

    def exit_program(self):
        self.cap.release()
        self.root.destroy()


if __name__ == "__main__":
    if len(sys.argv) < 2 or '-h' in sys.argv or '--help' in sys.argv:
        print("Usage: python video_kaleidoscope.py <video_path>\n")
        print("Controls:")
        print("  Play/Pause: Button to toggle between play and pause")
        print("  Stop: Button to stop the video")
        print("  Flip Horizontal: Button to flip the video horizontally")
        print("  Flip Vertical: Button to flip the video vertically")
        print("  Flip Up/Down: Button to flip the video vertically (upside down)")
        print("  Snapshot: Button to take a snapshot of the current frame")
        print("  Mirror Left: Button to cycle through mirror levels (center, thirds, quarters) on the left side")
        print("  Mirror Right: Button to cycle through mirror levels (center, thirds, quarters) on the right side")
        print("  Zoom In: Button to zoom in")
        print("  Zoom Out: Button to zoom out")
        print("  Frame Forward: Button to move forward one frame")
        print("  Frame Reverse: Button to move backward one frame")
        print("  Faster: Button to increase playback speed")
        print("  Slower: Button to decrease playback speed")
        print("  Pan Up: Button to pan up when zoomed in")
        print("  Pan Down: Button to pan down when zoomed in")
        print("  Pan Left: Button to pan left when zoomed in")
        print("  Pan Right: Button to pan right when zoomed in")
        print("  Center Pan: Button to recenter the panning position")
        print("  Reverse Playback: Button to increase reverse playback speed (up to 8x)")
        print("  LUT Selection: Dropdown to apply a color map (LUT) to the video")
        print("  Rotation Slider: Slider to adjust the rotation angle")
        print("  Zoom Slider: Slider to adjust the zoom level")
        print("  Kaleidoscope Segments Slider: Slider to adjust the number of kaleidoscope segments")
        sys.exit(1)

    video_path = sys.argv[1]
    vk = VideoKaleidoscope(video_path)
