from PIL import Image, ImageTk
import cv2
import tkinter as tk

class CameraApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Camera App")

        # Create a canvas to display the camera feed
        self.canvas = tk.Canvas(self.window, width=640, height=480)
        self.canvas.pack()

        # Open the camera
        self.cap = cv2.VideoCapture(0)

        # Start the camera feed
        self.update()
    
    

    def update(self):
        # Read a frame from the camera
        ret, frame = self.cap.read()

        if ret:
            # Convert the frame to an ImageTk object
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            # Update the canvas with the new image
            self.canvas.imgtk = imgtk
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)

            # Describe the objects in the image
            describe_image(frame)

        # Schedule the next update
        self.window.after(10, self.update)

    def run(self):
        # Start the main loop
        self.window.mainloop()

    def __del__(self):
        # Release the camera
        self.cap.release()

# Create the camera app
app = CameraApp()

# Run the camera app
app.run()
