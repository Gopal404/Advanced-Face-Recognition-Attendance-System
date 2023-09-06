import tkinter as tk
import cv2

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.is_running = False
        
        # Create start and stop buttons
        self.start_button = tk.Button(window, text="Start", width=25, command=self.start)
        self.start_button.pack(padx=5, pady=5)
        self.stop_button = tk.Button(window, text="Stop", width=25, command=self.stop)
        self.stop_button.pack(padx=5, pady=5)
        
        # Create OpenCV camera object
        self.cap = cv2.VideoCapture(0)
        
        # Create OpenCV image object
        self.image = None
        
        # Create canvas to display image
        self.canvas = tk.Canvas(window, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()
        
        # Start the Tkinter event loop
        self.window.mainloop()
        
    def start(self):
        self.is_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
        # Start the camera feed
        while self.is_running:
            ret, frame = self.cap.read()
            if ret:
                self.image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.photo = tk.PhotoImage(image=tk.Image.fromarray(self.image))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.window.update()
        
    def stop(self):
        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        
    def on_exit(self):
        self.cap.release()
        self.window.destroy()

# Create a window and launch the app
App(tk.Tk(), "Camera App")
