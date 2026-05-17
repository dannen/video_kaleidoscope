# Video Kaleidoscope

A real-time video art tool built with Python, OpenCV, and Tkinter. Load any video and sculpt it live with mirroring, rotation, zoom, color palettes, kaleidoscope blending, echo trails, pixel sorting, edge glow, and more. Designed for creative exploration and live performance.

## Requirements

Python 3.8+ and the following packages:

```sh
pip install opencv-python numpy Pillow
```

### Setting up a virtual environment (recommended)

Using a venv keeps the dependencies isolated from your system Python:

```sh
# Create the virtual environment (one time)
python3 -m venv .venv

# Activate it
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# Install dependencies
pip install opencv-python numpy Pillow

# Run the app (venv must be active)
python video_kaleidoscope.py <video_path>

# When you're done, deactivate
deactivate
```

Add `.venv/` to your `.gitignore` if you haven't already so the environment folder isn't committed.

## Usage

```sh
python video_kaleidoscope.py <video_path>
```

The main window shows the video output with a seek bar. A separate **Video Controls** window holds all the sliders and buttons.

---

## Controls

### Playback

| Button | Action |
|--------|--------|
| Play / Pause | Toggle playback |
| Reverse | Cycle reverse playback speed (1×, 2×, 4×, 8×) |
| Reset | Return all effects to defaults |
| Exit | Quit the application |

**Speed slider** (Adjustments panel) — positive values play forward, negative values play in reverse. Range: −4× to +4×.

**Seek bar** (main window) — drag to jump to any position in the video.

---

### Transforms

| Button | Action |
|--------|--------|
| Flip Horizontal | Mirror left–right |
| Flip Vertical | Mirror top–bottom |
| Flip Both | Flip horizontally and vertically together |
| Mirror Up | Copy the top half onto the bottom half |
| Mirror Down | Copy the bottom half onto the top half |
| Mirror Left | Cycle through left-side mirror levels: off → center split → thirds → quarters |
| Mirror Right | Cycle through right-side mirror levels: off → center split → thirds → quarters |

**Rot slider** — rotation angle, 0–359°, with 0.5° resolution.

**Zoom slider** — zoom factor from 1× to 5×.

**Pan controls** — Up / Down / Left / Right / Center buttons; active only when zoomed in.

---

### Adjustments Panel (vertical sliders)

| Slider | Range | Effect |
|--------|-------|--------|
| Rotation | 0–359° | Rotation angle |
| Zoom | −50 to +50 | Centre = 1× (no zoom). Right = zoom in (1×–6×). Left = same zoom level but frame is flipped on both axes first. |
| Speed | −4 to +4 | Playback speed. Positive = forward, negative = reverse, centre = very slow. |
| Brightness | −4 to +4 | Brightness offset |
| Hue Rotation | 0–359 | Hue shift applied in HSV space — rotates all colors without touching brightness or saturation |
| Auto Spin | −5 to +5 °/frame | Auto-rotate speed; increments the rotation angle every frame, works while paused |

---

### Effects Panel (horizontal sliders + dropdown)

| Control | Range | Effect |
|---------|-------|--------|
| Kaleidoscope | 0–12 segments | Blends N rotated copies of the frame for a rotational symmetry effect |
| Echo Decay | 0–95 | Feedback trail strength — each frame blends with the previous output at this percentage; high values create long psychedelic trails |
| Pixel Sort Threshold | 0–255 | Pixels in each row with luminance ≥ threshold are sorted by brightness, creating horizontal streaking and glitch art |
| Edge Glow | 0–100 | Canny edge detection overlaid as a cyan neon glow |
| LUT dropdown | — | Apply a color map to the video; includes built-in OpenCV colormaps, custom `.lut` files from `./luts/`, and any palettes loaded from `./color_palletes/` |

---

### Color Palettes

Place any PNG images in a folder named `color_palletes/` in the same directory as the script. On startup the app samples the middle row of each image, resamples it to 256 pixels, and registers it as a LUT named `PAL_<FILENAME>`. These appear in the LUT dropdown and can be cycled with the keyboard shortcuts below.

---

### Snapshot & Recording

| Control | Action |
|---------|--------|
| Snapshot button | Saves the current processed frame as `snapshot-YYYYMMDDHHMMSS.png` |
| **● REC** button | Starts recording every displayed frame to `recording-YYYYMMDDHHMMSS.avi`. Button turns red and reads **■ STOP REC**. Click again or exit to finalize the file. |

Snapshots and recordings are saved to the working directory and are excluded from git.

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `i` | Invert the current LUT (flip the color map) |
| `[` | Shift LUT colors left by 8 steps (cycles the gradient) |
| `]` | Shift LUT colors right by 8 steps |
| `p` | Next LUT (cycles through all LUTs: built-ins, `.lut` files, and `color_palletes/` images) |
| `P` | Previous LUT |

---

## Effect Pipeline Order

When processing each frame the effects are applied in this sequence:

1. Resize to display (max 800 × 600)
2. Zoom / pan crop
3. Rotation
4. Flip (horizontal / vertical)
5. Mirror (left, right, up, down)
6. Hue rotation
7. Brightness
8. Pixel sort
9. Kaleidoscope blend
10. LUT colormap
11. Echo feedback
12. Edge glow
13. Write to recording file (if active)
14. Display

---

## Custom LUT Files

Place `.lut` files in the `./luts/` directory. Each file must contain a single Python list of exactly 256 RGB 3-tuples, for example:

```python
[(255, 0, 0), (254, 1, 0), ..., (0, 0, 255)]
```

The filename (without extension) becomes the LUT name in the dropdown.

---

## Adding More Palettes

Drop any PNG into `color_palletes/` and restart the app. The image can be any size — the script samples a single horizontal strip from the vertical midpoint. Flat color-swatch images (bands of solid color) work especially well.
