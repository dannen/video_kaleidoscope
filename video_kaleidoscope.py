# Requires: pip install opencv-python numpy Pillow
import sys
from datetime import datetime
import threading
import collections
import tkinter as tk
from tkinter import OptionMenu, StringVar, Toplevel, Frame, LabelFrame
import cv2
import numpy as np
from PIL import Image, ImageTk
import os
import ast

LUTS = {
    'AUTUMN': cv2.COLORMAP_AUTUMN,
    'BONE': cv2.COLORMAP_BONE,
    'CIVIDIS': cv2.COLORMAP_CIVIDIS,
    'COOL': cv2.COLORMAP_COOL,
    'DEEPGREEN': cv2.COLORMAP_DEEPGREEN,
    'HOT': cv2.COLORMAP_HOT,
    'HSV': cv2.COLORMAP_HSV,
    'INFERNO': cv2.COLORMAP_INFERNO,
    'ISOTHERM_BLACKLIGHT': lambda: create_custom_lut('blacklight', 64),
    'ISOTHERM_BLUE': lambda: create_custom_lut('blue', 64),
    'ISOTHERM_CYAN': lambda: create_custom_lut('cyan', 64),
    'ISOTHERM_FOREST': lambda: create_custom_lut('forest', 64),
    'ISOTHERM_GREEN': lambda: create_custom_lut('green', 64),
    'ISOTHERM_MAGENTA': lambda: create_custom_lut('magenta', 64),
    'ISOTHERM_ORANGE': lambda: create_custom_lut('orange', 64),
    'ISOTHERM_PURPLE': lambda: create_custom_lut('purple', 64),
    'ISOTHERM_RED': lambda: create_custom_lut('red', 64),
    'ISOTHERM_TURQUOISE': lambda: create_custom_lut('turquoise', 64),
    'ISOTHERM_WARM_TO_COOL': lambda: create_custom_lut('warm_to_cool', 64),
    'ISOTHERM_YELLOW': lambda: create_custom_lut('yellow', 64),
    'JET': cv2.COLORMAP_JET,
    'MAGMA': cv2.COLORMAP_MAGMA,
    'OCEAN': cv2.COLORMAP_OCEAN,
    'PARULA': cv2.COLORMAP_PARULA,
    'PINK': cv2.COLORMAP_PINK,
    'PLASMA': cv2.COLORMAP_PLASMA,
    'RAINBOW': cv2.COLORMAP_RAINBOW,
    'SPRING': cv2.COLORMAP_SPRING,
    'SUMMER': cv2.COLORMAP_SUMMER,
    'TURBO': cv2.COLORMAP_TURBO,
    'TWILIGHT': cv2.COLORMAP_TWILIGHT,
    'VIRIDIS': cv2.COLORMAP_VIRIDIS,
    'WINTER': cv2.COLORMAP_WINTER
}

# Load custom LUTs from a directory
lut_directory = "./luts"
for filename in os.listdir(lut_directory):
    if filename.endswith('.lut'):
        filepath = os.path.join(lut_directory, filename)
        try:
            with open(filepath, 'r') as f:
                # Expect the file to contain only a list of tuples
                lut_data = f.read().strip()
                if lut_data.startswith('[') and lut_data.endswith(']'):
                    lut_values = ast.literal_eval(lut_data)
                    if isinstance(lut_values, list) and all(isinstance(color, tuple) and len(color) == 3 for color in lut_values):
                        lut_name = os.path.splitext(filename)[0]
                        lut_array = np.array(
                            lut_values, dtype=np.uint8).reshape((256, 1, 3))
                        LUTS[lut_name] = lut_array
                        print(f"Loaded custom LUT: {lut_name}")
                    else:
                        print(
                            f"Invalid format in LUT file: {filename}. Expected a list of 3-tuple colors.")
                else:
                    print(
                        f"Invalid format in LUT file: {filename}. File must contain a list of color tuples.")
        except (SyntaxError, ValueError) as e:
            print(f"Error loading LUT file {filename}: {e}")
        except Exception as e:
            print(f"Unexpected error loading LUT file {filename}: {e}")

# Load palette LUTs from color_palletes directory (not tracked in git)
PALETTE_LUT_NAMES = []
palette_directory = "./color_palletes"
if os.path.isdir(palette_directory):
    for filename in sorted(os.listdir(palette_directory)):
        if filename.lower().endswith('.png'):
            filepath = os.path.join(palette_directory, filename)
            try:
                img = Image.open(filepath).convert('RGB')
                w, h = img.size
                middle_row = img.crop((0, h // 2, w, h // 2 + 1)).resize((256, 1), Image.LANCZOS)
                lut_array = np.array(middle_row, dtype=np.uint8).reshape((256, 1, 3))
                lut_name = f"PAL_{os.path.splitext(filename)[0].upper()}"
                LUTS[lut_name] = lut_array
                PALETTE_LUT_NAMES.append(lut_name)
                print(f"Loaded palette LUT: {lut_name}")
            except Exception as e:
                print(f"Error loading palette {filename}: {e}")


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
    elif color == 'turquoise':
        gradient_colors = ((64, 64, 0), (255, 255, 0), color_gradient_step)
    elif color == 'yellow':
        gradient_colors = ((0, 32, 64), (0, 255, 255), color_gradient_step)
    elif color == 'magenta':
        gradient_colors = ((64, 0, 64), (255, 0, 255), color_gradient_step)
    elif color == 'orange':
        gradient_colors = ((0, 64, 64), (0, 128, 255), color_gradient_step)
    elif color == 'cyan':
        gradient_colors = ((64, 32, 0), (255, 128, 0), color_gradient_step)
    elif color == 'purple':
        gradient_colors = ((64, 0, 64), (255, 0, 128), color_gradient_step)
    elif color == 'warm_to_cool':
        gradient_colors = ((255, 0, 0), (0, 0, 255), color_gradient_step)
    elif color == 'blacklight':
        gradient_colors = ((0, 64, 255), (128, 0, 128), color_gradient_step)
    elif color == 'forest':
        gradient_colors = ((0, 128, 0), (139, 69, 19), color_gradient_step)
    else:
        raise ValueError(
            "Unsupported color for LUT creation. Supported colors are 'red', 'green', 'blue', etc.")

    black_to_white_step = 256 - color_gradient_step
    black_to_white = np.linspace(
        (0, 0, 0), (255, 255, 255), black_to_white_step).astype(np.uint8)
    color_gradient = np.linspace(*gradient_colors).astype(np.uint8)
    custom_colors = np.concatenate((black_to_white, color_gradient))

    # Ensure we have exactly 256 colors by interpolating if necessary
    if len(custom_colors) != 256:
        custom_colors = np.linspace(
            custom_colors[0], custom_colors[-1], 256, axis=0).astype(np.uint8)

    # Create a custom LUT with 256 entries
    custom_lut = custom_colors.reshape((256, 1, 3))
    return custom_lut


class VideoAttributes:
    def __init__(self):
        self.mirror_left_level = 0
        self.mirror_right_level = 0
        self.flip_horizontal = False
        self.flip_vertical = False
        self.mirror_up = False
        self.mirror_down = False
        self.rotation_angle = 0
        self.playback_speed = 1.0
        self.reverse_playback_speed = 1.0
        self.zoom_factor = 1.0
        self.paused = False
        self.pan_x = 0
        self.pan_y = 0
        self.kaleidoscope_segments = 0
        self.brightness = 0
        self.hue_rotation = 0
        self.auto_rotate_speed = 0.0
        self.echo_strength = 0
        self.pixel_sort_threshold = 0
        self.edge_glow_intensity = 0


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
        self.base_lut = None
        self.modified_lut = cv2.applyColorMap(
            np.arange(256, dtype=np.uint8), cv2.COLORMAP_RAINBOW
        )
        self.echo_frame = None
        self.recording = False
        self.video_writer = None
        self.root = tk.Tk()
        self.root.title("Video Kaleidoscope")

        # Set up video display area
        self.video_label = tk.Label(self.root)
        self.video_label.pack()

        # Slider for video position (seek bar)
        self.seek_slider = tk.Scale(self.root, from_=0, to=1000, orient=tk.HORIZONTAL,
                                    label="Video Position", command=self.set_video_position)
        self.seek_slider.pack(fill=tk.X)

        # Set up controls in separate windows
        self.create_control_window()

        # Add key bindings for LUT manipulations
        self.root.bind("i", self.invert_lut)
        self.root.bind("[", self.shift_lut_left)
        self.root.bind("]", self.shift_lut_right)

        # Palette cycling (p = next, P = previous)
        self.palette_index = -1
        self.root.bind("p", self.cycle_palette_forward)
        self.root.bind("P", self.cycle_palette_backward)

        # Start updating video
        self.update_video()

        self.root.mainloop()

    def apply_modified_lut(self):
        """Applies modifications to the base LUT and updates the modified LUT."""
        if isinstance(self.base_lut, int):
            # OpenCV colormap LUTs (predefined) are integers
            self.modified_lut = self.base_lut
        elif self.base_lut is not None:
            # Custom LUTs are NumPy arrays
            self.modified_lut = self.base_lut.copy()

    def invert_lut(self, event=None):
        """Invert the LUT."""
        if self.modified_lut is not None:
            self.modified_lut = np.flip(self.modified_lut, axis=0)
        else:
            print("Error: LUT not properly initialized.")

    def shift_lut_left(self, event=None):
        """Shift LUT values to the left."""
        if self.modified_lut is not None and self.modified_lut.ndim == 3:
            self.modified_lut = np.roll(self.modified_lut, -8, axis=0)
        else:
            print("Error: LUT not properly initialized.")

    def shift_lut_right(self, event=None):
        """Shift LUT values to the right."""
        if self.modified_lut is not None and self.modified_lut.ndim == 3:
            self.modified_lut = np.roll(self.modified_lut, 8, axis=0)
        else:
            print("Error: LUT not properly initialized.")

    def set_hue_rotation(self, value):
        self.attributes.hue_rotation = value
        if self.attributes.paused:
            self.apply_effects()

    def set_auto_rotate_speed(self, value):
        self.attributes.auto_rotate_speed = value

    def set_echo_strength(self, value):
        self.attributes.echo_strength = value
        if value == 0:
            self.echo_frame = None

    def set_pixel_sort_threshold(self, value):
        self.attributes.pixel_sort_threshold = value
        if self.attributes.paused:
            self.apply_effects()

    def set_edge_glow_intensity(self, value):
        self.attributes.edge_glow_intensity = value
        if self.attributes.paused:
            self.apply_effects()

    def toggle_recording(self):
        if self.recording:
            self.recording = False
            if self.video_writer:
                self.video_writer.release()
                self.video_writer = None
                print('Recording saved.')
            self.record_button.config(text="● REC", fg="red")
        else:
            self.recording = True
            self.video_writer = None  # created on first frame
            self.record_button.config(text="■ STOP REC", fg="white", bg="red")

    def apply_hue_rotation(self, frame):
        if self.attributes.hue_rotation == 0:
            return frame
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.int16)
        hsv[:, :, 0] = (hsv[:, :, 0] + self.attributes.hue_rotation // 2) % 180
        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    def apply_pixel_sort(self, frame):
        threshold = self.attributes.pixel_sort_threshold
        if threshold == 0:
            return frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result = frame.copy()
        for y in range(frame.shape[0]):
            lum = gray[y]
            idxs = np.where(lum >= threshold)[0]
            if len(idxs) == 0:
                continue
            result[y, idxs] = frame[y, idxs[np.argsort(lum[idxs])]]
        return result

    def apply_echo(self, frame):
        strength = self.attributes.echo_strength / 100.0
        if strength == 0.0:
            return frame
        if self.echo_frame is None or self.echo_frame.shape != frame.shape:
            self.echo_frame = frame.copy()
            return frame
        result = cv2.addWeighted(frame, 1.0 - strength, self.echo_frame, strength, 0)
        self.echo_frame = result.copy()
        return result

    def apply_edge_glow(self, frame):
        intensity = self.attributes.edge_glow_intensity
        if intensity == 0:
            return frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        glow = np.zeros_like(frame)
        glow[:, :, 0] = edges  # B
        glow[:, :, 1] = edges  # G  → cyan glow (B+G in BGR)
        return cv2.addWeighted(frame, 1.0, glow, intensity / 100.0, 0)

    def cycle_palette_forward(self, event=None):
        if not PALETTE_LUT_NAMES:
            return
        self.palette_index = (self.palette_index + 1) % len(PALETTE_LUT_NAMES)
        name = PALETTE_LUT_NAMES[self.palette_index]
        self.lut_var.set(name)
        self.set_lut(name)

    def cycle_palette_backward(self, event=None):
        if not PALETTE_LUT_NAMES:
            return
        self.palette_index = (self.palette_index - 1) % len(PALETTE_LUT_NAMES)
        name = PALETTE_LUT_NAMES[self.palette_index]
        self.lut_var.set(name)
        self.set_lut(name)

    def _apply_transforms(self, frame):
        """Apply zoom/pan, rotation, flip, and all mirror effects to frame, preserving its dimensions."""
        h, w = frame.shape[:2]

        # Zoom and pan (negative zoom_factor = same crop + flip both axes)
        zoom = abs(self.attributes.zoom_factor)
        cx = w // 2 + self.attributes.pan_x
        cy = h // 2 + self.attributes.pan_y
        nw = int(w / zoom)
        nh = int(h / zoom)
        x1, y1 = max(0, cx - nw // 2), max(0, cy - nh // 2)
        x2, y2 = min(w, cx + nw // 2), min(h, cy + nh // 2)
        frame = cv2.resize(frame[y1:y2, x1:x2], (w, h))
        if self.attributes.zoom_factor < 0:
            frame = cv2.flip(frame, -1)

        # Rotation
        if self.attributes.rotation_angle != 0:
            matrix = cv2.getRotationMatrix2D((w // 2, h // 2), self.attributes.rotation_angle, 1)
            frame = cv2.warpAffine(frame, matrix, (w, h), borderMode=cv2.BORDER_REFLECT)

        # Flip
        if self.attributes.flip_horizontal:
            frame = cv2.flip(frame, 1)
        if self.attributes.flip_vertical:
            frame = cv2.flip(frame, 0)

        # Mirror left
        if self.attributes.mirror_left_level == 1:
            frame[:, w // 2:] = cv2.flip(frame[:, :w // 2], 1)
        elif self.attributes.mirror_left_level == 2:
            tw = w // 3
            left, right = frame[:, :tw].copy(), frame[:, 2 * tw:].copy()
            min_w = min(tw, right.shape[1])
            frame[:, tw:tw + min_w] = cv2.flip(left[:, :min_w], 1)
            frame[:, :min_w] = cv2.flip(right[:, :min_w], 1)
        elif self.attributes.mirror_left_level == 3:
            qw = w // 4
            for i in range(0, 4, 2):
                frame[:, i * qw:(i + 1) * qw] = cv2.flip(frame[:, i * qw:(i + 1) * qw].copy(), 1)

        # Mirror right
        if self.attributes.mirror_right_level == 1:
            frame[:, :w // 2] = cv2.flip(frame[:, w // 2:], 1)
        elif self.attributes.mirror_right_level == 2:
            tw = w // 3
            left, right = frame[:, :tw].copy(), frame[:, 2 * tw:].copy()
            min_w = min(tw, right.shape[1])
            frame[:, tw:tw + min_w] = cv2.flip(right[:, :min_w], 1)
            frame[:, 2 * tw:2 * tw + min_w] = cv2.flip(left[:, :min_w], 1)
        elif self.attributes.mirror_right_level == 3:
            qw = w // 4
            for i in range(1, 4, 2):
                frame[:, i * qw:(i + 1) * qw] = cv2.flip(frame[:, i * qw:(i + 1) * qw].copy(), 1)

        # Mirror up/down
        if self.attributes.mirror_up:
            frame[h // 2:, :] = cv2.flip(frame[:h // 2, :], 0)
        if self.attributes.mirror_down:
            frame[:h // 2, :] = cv2.flip(frame[h // 2:, :], 0)

        return frame

    def create_control_window(self):
        self.control_window = Toplevel(self.root)
        self.control_window.title("Video Controls")
        self.control_window.geometry("520x900+200+800")

        # Control section for play, pause, etc.
        controls_frame = LabelFrame(self.control_window, text="Controls")
        controls_frame.pack(fill=tk.X, padx=5, pady=5, ipadx=10)

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
            flip_inverse_icon = ImageTk.PhotoImage(
                Image.open("icons/flip_up_down.png").resize((25, 25)))
            snapshot_icon = ImageTk.PhotoImage(Image.open(
                "icons/snapshot_button.png").resize((25, 25)))
            mirror_left_icon = ImageTk.PhotoImage(
                Image.open("icons/mirror_left.png").resize((25, 25)))
            mirror_right_icon = ImageTk.PhotoImage(
                Image.open("icons/mirror_right.png").resize((25, 25)))
            mirror_up_icon = ImageTk.PhotoImage(
                Image.open("icons/mirror_up.png").resize((25, 25)))
            mirror_down_icon = ImageTk.PhotoImage(
                Image.open("icons/mirror_down.png").resize((25, 25)))
            exit_icon = ImageTk.PhotoImage(Image.open(
                "icons/exit_button.png").resize((25, 25)))
            reset_icon = ImageTk.PhotoImage(Image.open(
                "icons/reset_button.png").resize((25, 25)))
            reverse_playback_icon = ImageTk.PhotoImage(
                Image.open("icons/reverse_playback.png").resize((25, 25)))
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
        except FileNotFoundError as e:
            print(f"Error: {e}")
            sys.exit(1)

        # Buttons for controls with icons
        top_row_controls = [
            (play_icon, self.toggle_pause),
            (pause_icon, self.toggle_pause),
            (reverse_playback_icon, self.toggle_reverse_playback_speed),
            (exit_icon, self.exit_program)
        ]
        second_row_controls = [
            (flip_horizontal_icon, self.toggle_flip_horizontal),
            (flip_vertical_icon, self.toggle_flip_vertical),
            (flip_inverse_icon, self.toggle_flip_inverse),
            (snapshot_icon, self.snapshot),
            (reset_icon, self.reset)
        ]
        third_row_controls = [
            (mirror_up_icon, self.toggle_mirror_up),
            (mirror_down_icon, self.toggle_mirror_down),
            (mirror_left_icon, lambda: self.toggle_mirror_level('left')),
            (mirror_right_icon, lambda: self.toggle_mirror_level('right'))
        ]

        # Add top row controls
        for idx, (icon, command) in enumerate(top_row_controls):
            tk.Button(controls_frame, image=icon, command=command).grid(
                row=0, column=idx, padx=5, pady=5, sticky='ew')

        # Add second row controls
        for idx, (icon, command) in enumerate(second_row_controls):
            tk.Button(controls_frame, image=icon, command=command).grid(
                row=1, column=idx, padx=5, pady=5)

        # Add third row controls for mirror buttons
        for idx, (icon, command) in enumerate(third_row_controls):
            tk.Button(controls_frame, image=icon, command=command).grid(
                row=2, column=idx, padx=5, pady=5)

        # Record button (4th row)
        self.record_button = tk.Button(
            controls_frame, text="● REC", fg="red", command=self.toggle_recording, width=10)
        self.record_button.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky='ew')

        # Sliders section
        sliders_frame = LabelFrame(self.control_window, text="Adjustments")
        sliders_frame.pack(fill=tk.X, padx=5, pady=5, ipadx=10)

        self.rotation_slider = tk.Scale(sliders_frame, from_=0, to=359.5, orient=tk.HORIZONTAL,
                                        resolution=0.5, label="Rotation",
                                        command=lambda x: self.set_rotation_angle(float(x)))
        self.rotation_slider.pack(fill=tk.X, padx=5, pady=2)

        # Zoom: centre (0) = 1× no flip; right = zoom in; left = zoom in + flip both axes
        self.zoom_slider = tk.Scale(sliders_frame, from_=-50, to=50, orient=tk.HORIZONTAL,
                                    label="Zoom  (negative = flip)",
                                    command=lambda x: self.set_zoom_factor(float(x)))
        self.zoom_slider.pack(fill=tk.X, padx=5, pady=2)

        self.playback_speed_slider = tk.Scale(sliders_frame, from_=-4.0, to=4.0, orient=tk.HORIZONTAL,
                                              resolution=0.1, label="Speed  (negative = reverse)",
                                              command=lambda x: self.set_playback_speed(float(x)))
        self.playback_speed_slider.pack(fill=tk.X, padx=5, pady=2)

        self.brightness_slider = tk.Scale(sliders_frame, from_=-4, to=4, orient=tk.HORIZONTAL,
                                          label="Brightness",
                                          command=lambda x: self.set_brightness(int(x)))
        self.brightness_slider.pack(fill=tk.X, padx=5, pady=2)

        self.hue_slider = tk.Scale(sliders_frame, from_=0, to=359, orient=tk.HORIZONTAL,
                                   label="Hue Rotation",
                                   command=lambda x: self.set_hue_rotation(int(x)))
        self.hue_slider.pack(fill=tk.X, padx=5, pady=2)

        self.spin_slider = tk.Scale(sliders_frame, from_=-5.0, to=5.0, orient=tk.HORIZONTAL,
                                    resolution=0.1, label="Auto Spin  (°/frame)",
                                    command=lambda x: self.set_auto_rotate_speed(float(x)))
        self.spin_slider.pack(fill=tk.X, padx=5, pady=2)

        # Kaleidoscope and LUT section
        kaleidoscope_frame = LabelFrame(self.control_window, text="Effects")
        kaleidoscope_frame.pack(fill=tk.X, padx=5, pady=5, ipadx=10)

        self.kaleidoscope_slider = tk.Scale(kaleidoscope_frame, from_=0, to=12, orient=tk.HORIZONTAL,
                                            label="Kaleidoscope", command=lambda x: self.set_kaleidoscope_segments(int(x)))
        self.kaleidoscope_slider.pack(fill=tk.X, padx=5, pady=5)

        self.echo_slider = tk.Scale(kaleidoscope_frame, from_=0, to=95, orient=tk.HORIZONTAL,
                                    label="Echo Decay", command=lambda x: self.set_echo_strength(int(x)))
        self.echo_slider.pack(fill=tk.X, padx=5, pady=2)

        self.pixel_sort_slider = tk.Scale(kaleidoscope_frame, from_=0, to=255, orient=tk.HORIZONTAL,
                                          label="Pixel Sort Threshold", command=lambda x: self.set_pixel_sort_threshold(int(x)))
        self.pixel_sort_slider.pack(fill=tk.X, padx=5, pady=2)

        self.edge_glow_slider = tk.Scale(kaleidoscope_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                         label="Edge Glow", command=lambda x: self.set_edge_glow_intensity(int(x)))
        self.edge_glow_slider.pack(fill=tk.X, padx=5, pady=2)

        # LUT selection dropdown at the bottom
        self.lut_var = StringVar(self.control_window)
        self.lut_var.set("None")  # Default value
        luts = ["None"] + sorted(list(LUTS.keys()))
        self.lut_menu = OptionMenu(
            kaleidoscope_frame, self.lut_var, *luts, command=self.set_lut)
        self.lut_menu.pack(fill=tk.X, pady=5)

        # Pan controls section
        pan_frame = LabelFrame(self.control_window, text="Pan Controls")
        pan_frame.pack(fill=tk.X, padx=5, pady=5, ipadx=10)

        # Pan controls arranged in a plus shape
        tk.Button(pan_frame, image=pan_up_icon, command=lambda: self.pan_video(
            0, -10)).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(pan_frame, image=pan_left_icon, command=lambda: self.pan_video(-10, 0)
                  ).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(pan_frame, image=pan_center_icon, command=self.center_pan).grid(
            row=1, column=1, padx=5, pady=5)
        tk.Button(pan_frame, image=pan_right_icon, command=lambda: self.pan_video(
            10, 0)).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(pan_frame, image=pan_down_icon, command=lambda: self.pan_video(
            0, 10)).grid(row=2, column=1, padx=5, pady=5)

        # Keep references to the images to prevent garbage collection
        self.icons = [icon for icon, _ in top_row_controls +
                      second_row_controls + third_row_controls]
        self.icons += [pan_up_icon, pan_down_icon,
                       pan_left_icon, pan_right_icon, pan_center_icon]

    def set_video_position(self, position):
        if self.cap.isOpened():
            total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_number = int((int(position) / 1000.0) * total_frames)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame
                self.apply_effects()

    def update_seek_slider(self):
        if self.cap.isOpened():
            total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            position = int((current_frame / total_frames) * 1000)
            self.seek_slider.set(position)

    def set_kaleidoscope_segments(self, segments):
        self.attributes.kaleidoscope_segments = segments
        if self.attributes.paused:
            self.apply_effects()

    def set_brightness(self, brightness):
        self.attributes.brightness = brightness
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

    def toggle_flip_inverse(self):
        # Flip horizontally
        self.toggle_flip_horizontal()
        # Flip vertically
        self.toggle_flip_vertical()
        # Apply the effects after both flips
        self.apply_effects()

    def toggle_mirror_up(self):
        self.attributes.mirror_up = not self.attributes.mirror_up
        if self.attributes.paused:
            self.apply_effects()

    def toggle_mirror_down(self):
        self.attributes.mirror_down = not self.attributes.mirror_down
        if self.attributes.paused:
            self.apply_effects()

    def set_rotation_angle(self, angle):
        self.attributes.rotation_angle = angle % 360
        if self.attributes.paused:
            self.apply_effects()

    def set_playback_speed(self, speed):
        if speed < 0:
            self.attributes.reverse_playback_speed = abs(speed)
            self.attributes.playback_speed = 1.0
        else:
            self.attributes.playback_speed = max(0.05, min(speed, 16.0))
            self.attributes.reverse_playback_speed = 1.0

    def set_zoom_factor(self, value):
        # Slider -50..50: magnitude maps to 1.0 + abs(value)/10 zoom;
        # negative values additionally flip both axes.
        zoom = 1.0 + abs(value) / 10.0
        self.attributes.zoom_factor = zoom if value >= 0 else -zoom
        if self.attributes.paused:
            self.apply_effects()

    def pan_video(self, delta_x, delta_y):
        if abs(self.attributes.zoom_factor) > 1.0:
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
            self.base_lut = None
            self.modified_lut = None
        else:
            lut_function = LUTS.get(lut_name)
            if lut_function is None:
                print(f"Error: LUT '{lut_name}' not found.")
                return
            self.base_lut = lut_function() if callable(lut_function) else lut_function
            self.apply_modified_lut()
        if self.attributes.paused:
            self.apply_effects()

    def apply_lut(self, frame):
        if self.modified_lut is not None:
            if isinstance(self.modified_lut, np.ndarray):
                if self.modified_lut.shape == (256, 1, 3):
                    frame = cv2.LUT(frame, self.modified_lut)
                else:
                    print("Error: LUT must have shape (256, 1, 3).")
            else:
                frame = cv2.applyColorMap(frame, self.modified_lut)
        return frame

    def snapshot(self):
        if self.current_frame is None:
            return
        frame = self.apply_lut(self._apply_transforms(self.current_frame.copy()))
        timestamp = datetime.now().strftime('%Y%m%d%M%S')
        filename = f'snapshot-{timestamp}.png'
        threading.Thread(target=cv2.imwrite, args=(filename, frame)).start()
        print(f'Snapshot saving in progress as {filename}')

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
        if self.current_frame is None:
            return
        frame = self.current_frame.copy()
        h, w = frame.shape[:2]

        if w > 800 or h > 600:
            frame = cv2.resize(frame, (800, 600))

        frame = self._apply_transforms(frame)
        frame = self.apply_hue_rotation(frame)
        frame = cv2.convertScaleAbs(frame, alpha=1, beta=self.attributes.brightness * 25)
        frame = self.apply_pixel_sort(frame)

        if self.attributes.kaleidoscope_segments > 0:
            frame = self.kaleidoscope_effect(frame)

        frame = self.apply_lut(frame)
        frame = self.apply_echo(frame)
        frame = self.apply_edge_glow(frame)

        if self.recording:
            if self.video_writer is None:
                fh, fw = frame.shape[:2]
                ts = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f'recording-{ts}.avi'
                self.video_writer = cv2.VideoWriter(
                    filename, cv2.VideoWriter_fourcc(*'XVID'), 30.0, (fw, fh))
                print(f'Recording to: {filename}')
            self.video_writer.write(frame)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
        self.update_seek_slider()

    def kaleidoscope_effect(self, frame):
        height, width = frame.shape[:2]
        center_x, center_y = width // 2, height // 2
        mask = np.zeros_like(frame)

        angle_step = 360 // self.attributes.kaleidoscope_segments
        for i in range(self.attributes.kaleidoscope_segments):
            angle = i * angle_step
            matrix = cv2.getRotationMatrix2D((center_x, center_y), angle, 1)
            rotated = cv2.warpAffine(frame, matrix, (width, height))
            alpha = 1.0 / self.attributes.kaleidoscope_segments
            mask = cv2.addWeighted(mask, 1.0, rotated, alpha, 0)

        return mask

    def update_video(self):
        if self.attributes.auto_rotate_speed != 0.0:
            self.attributes.rotation_angle = (
                self.attributes.rotation_angle + self.attributes.auto_rotate_speed) % 360
            self.rotation_slider.set(self.attributes.rotation_angle)
            if self.attributes.paused:
                self.apply_effects()

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

        self.root.after(
            int(1000 / (30 * self.attributes.playback_speed)), self.update_video)

    def reset(self):
        self.attributes = VideoAttributes()
        self.echo_frame = None
        self.palette_index = -1
        self.lut_var.set("None")
        self.set_lut("None")
        for slider, value in [
            (self.rotation_slider, 0),
            (self.zoom_slider, 0),
            (self.playback_speed_slider, 1.0),
            (self.brightness_slider, 0),
            (self.hue_slider, 0),
            (self.spin_slider, 0),
            (self.kaleidoscope_slider, 0),
            (self.echo_slider, 0),
            (self.pixel_sort_slider, 0),
            (self.edge_glow_slider, 0),
        ]:
            slider.set(value)
        self.record_button.config(text="● REC", fg="red", bg=self.control_window.cget("bg"))
        if self.attributes.paused:
            self.apply_effects()

    def exit_program(self):
        self.cap.release()
        if self.video_writer:
            self.video_writer.release()
        self.root.destroy()


if __name__ == "__main__":
    if len(sys.argv) < 2 or '-h' in sys.argv or '--help' in sys.argv:
        print("Usage: python video_kaleidoscope.py <video_path>\n")
        print("Controls:")
        print("  Play/Pause: Button to toggle between play and pause")
        print("  Stop: Button to stop the video")
        print("  Flip Horizontal: Button to flip the video horizontally")
        print("  Flip Vertical: Button to flip the video vertically")
        print("  Mirror Up: Button to mirror the top half to the bottom")
        print("  Mirror Down: Button to mirror the bottom half to the top")
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
        print("  Brightness Slider: Slider to adjust the brightness level")
        print(
            "  Kaleidoscope Segments: Slider to adjust the number of kaleidoscope segments")
        sys.exit(1)
    else:
        video_path = sys.argv[1]
        VideoKaleidoscope(video_path)
