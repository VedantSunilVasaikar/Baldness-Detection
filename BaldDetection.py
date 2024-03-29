import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO
import torch

model = YOLO("bald.pt")

def preprocess_image(image):
    image = cv2.resize(image, (192, 192))
    image = image / 255.0 
    image = torch.from_numpy(image).permute(2, 0, 1).float()
    return image.unsqueeze(0)

def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = cv2.imread(file_path)
        image = cv2.resize(image, (300, 300))  # Resize for display
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        detect_baldness(file_path)

def detect_baldness(file_path):
    frame = cv2.imread(file_path)
    frame_preprocessed = preprocess_image(frame)

    results = model.predict(frame_preprocessed)

    for r in results:
        im_array = r.plot()
        im = Image.fromarray(im_array)
        imgtk = ImageTk.PhotoImage(image=im)

        result_label.configure(image=imgtk)
        result_label.image = imgtk

root = tk.Tk()
root.title("Baldness Detection")
root.geometry("720x720")

upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack(pady=10)

result_label = tk.Label(root)
result_label.pack(pady=10)

root.mainloop()






