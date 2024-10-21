from PIL import Image, ImageDraw
import os

def create_icon(draw_function, filename):
    os.makedirs('icons', exist_ok=True)
    image = Image.new('RGB', (25, 25), 'white')
    draw = ImageDraw.Draw(image)
    draw_function(draw)
    image.save(os.path.join('icons', filename))

def draw_play_button(draw):
    draw.polygon([(8, 5), (8, 20), (20, 12)], fill='red')

def draw_pause_button(draw):
    draw.rectangle([(7, 5), (10, 20)], fill='black')
    draw.rectangle([(15, 5), (18, 20)], fill='black')

def draw_stop_button(draw):
    draw.rectangle([(7, 7), (18, 18)], fill='black')

def draw_flip_horizontal(draw):
    draw.line([(5, 12), (20, 12)], fill='black', width=2)
    draw.polygon([(15, 8), (20, 12), (15, 16)], fill='red')

def draw_flip_vertical(draw):
    draw.line([(12, 5), (12, 20)], fill='black', width=2)
    draw.polygon([(8, 15), (12, 20), (16, 15)], fill='red')

def draw_snapshot_button(draw):
    draw.rectangle([(5, 8), (20, 17)], outline='black', width=2)
    draw.rectangle([(10, 5), (15, 10)], fill='black')

def draw_mirror_left(draw):
    draw.line([(18, 5), (18, 20)], fill='black', width=2)
    draw.polygon([(10, 12), (15, 8), (15, 16)], fill='red')

def draw_mirror_right(draw):
    draw.line([(8, 5), (8, 20)], fill='black', width=2)
    draw.polygon([(12, 8), (17, 12), (12, 16)], fill='red')

def draw_rotate_left(draw):
    draw.arc([5, 5, 20, 20], start=270, end=90, fill='black', width=2)
    draw.polygon([(12, 5), (16, 9), (8, 9)], fill='red')

def draw_rotate_right(draw):
    draw.arc([5, 5, 20, 20], start=90, end=-90, fill='black', width=2)
    draw.polygon([(12, 5), (8, 9), (16, 9)], fill='red')

def draw_zoom_in(draw):
    draw.ellipse([(3, 3), (21, 21)], outline='black', width=2)
    draw.line([(12, 8), (12, 16)], fill='red', width=2)
    draw.line([(8, 12), (16, 12)], fill='red', width=2)

def draw_zoom_out(draw):
    draw.ellipse([(3, 3), (21, 21)], outline='black', width=2)
    draw.line([(8, 12), (16, 12)], fill='red', width=2)

def draw_frame_forward(draw):
    draw.line([(8, 5), (8, 20)], fill='black', width=2)
    draw.polygon([(10, 8), (17, 12), (10, 16)], fill='red')

def draw_frame_reverse(draw):
    draw.polygon([(18, 7), (9, 12), (18, 17)], fill='red')
    draw.line([(17, 5), (17, 20)], fill='black', width=2)

def draw_exit_button(draw):
    draw.rectangle([(6, 5), (14, 20)], outline='black', width=2)
    draw.polygon([(15, 12), (20, 10), (20, 14)], fill='red')

def draw_pan_up(draw):
    draw.polygon([(12, 5), (5, 20), (19, 20)], outline='red', width=2)

def draw_pan_down(draw):
    draw.polygon([(12, 20), (5, 5), (19, 5)], outline='red', width=2)

def draw_pan_right(draw):
    draw.polygon([(20, 12), (5, 5), (5, 19)], outline='red', width=2)

def draw_pan_left(draw):
    draw.polygon([(5, 12), (20, 5), (20, 19)], outline='red', width=2)

def draw_center(draw):
    draw.ellipse([(5, 5), (20, 20)], outline='black', width=2)
    draw.ellipse([(10, 10), (15, 15)], fill='red')

def main():
    icons = [
        (draw_play_button, 'play_button.png'),
        (draw_pause_button, 'pause_button.png'),
        (draw_stop_button, 'stop_button.png'),
        (draw_flip_horizontal, 'flip_horizontal.png'),
        (draw_flip_vertical, 'flip_vertical.png'),
        (draw_snapshot_button, 'snapshot_button.png'),
        (draw_mirror_left, 'mirror_left.png'),
        (draw_mirror_right, 'mirror_right.png'),
        (draw_rotate_left, 'rotate_left.png'),
        (draw_rotate_right, 'rotate_right.png'),
        (draw_zoom_in, 'zoom_in.png'),
        (draw_zoom_out, 'zoom_out.png'),
        (draw_frame_forward, 'frame_forward.png'),
        (draw_frame_reverse, 'frame_reverse.png'),
        (draw_exit_button, 'exit_button.png'),
        (draw_pan_up, 'pan_up.png'),
        (draw_pan_down, 'pan_down.png'),
        (draw_pan_right, 'pan_right.png'),
        (draw_pan_left, 'pan_left.png'),
        (draw_center, 'pan_center.png'),
    ]

    for draw_function, filename in icons:
        create_icon(draw_function, filename)

if __name__ == "__main__":
    main()
