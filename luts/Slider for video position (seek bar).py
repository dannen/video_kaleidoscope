# Slider for video position (seek bar)
self.seek_slider = Scale(self.root, from_=0, to=1000, orient=HORIZONTAL,
                         label="Video Position", command=self.set_video_position)
self.seek_slider.pack(fill=tk.X)


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
