import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os

class ImageEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("N3thunt3r69's Pixel Manipulator")
        self.root.geometry("600x400")
        self.root.config(bg="#2c3e50")
        
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg="#2c3e50")
        self.main_frame.pack(expand=True, fill="both")
        
        # Create upload frame
        self.upload_frame = tk.Frame(self.main_frame, bg="#2c3e50")
        self.upload_frame.pack(pady=20)
        
        # Create canvas for image display
        self.canvas = tk.Canvas(self.main_frame, bg="#34495e", highlightthickness=0)
        self.canvas.pack(expand=True, fill="both")
        
        # Create buttons and key input field
        self.upload_button = tk.Button(self.upload_frame, text="Upload Image", command=self.upload_image, bg="#3498db", fg="#ffffff", padx=10, pady=5)
        self.upload_button.grid(row=0, column=0, padx=10)
        
        self.encrypt_button = tk.Button(self.upload_frame, text="Encrypt", command=self.encrypt_image, bg="#2ecc71", fg="#ffffff", padx=10, pady=5)
        self.encrypt_button.grid(row=0, column=1, padx=10)
        
        self.decrypt_button = tk.Button(self.upload_frame, text="Decrypt", command=self.decrypt_image, bg="#e74c3c", fg="#ffffff", padx=10, pady=5)
        self.decrypt_button.grid(row=0, column=2, padx=10)

        self.key_label = tk.Label(self.upload_frame, text="Encryption Key:", bg="#2c3e50", fg="#ffffff")
        self.key_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.key_entry = tk.Entry(self.upload_frame, show="*", width=20)
        self.key_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Bind mouse drag events
        self.canvas.bind("<B1-Motion>", self.drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self.drag_release)

        self.image_path = None
        self.img = None
        self.displayed_image = None
        self.drag_data = {"x": 0, "y": 0, "item": None}
    
    def upload_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.img = Image.open(self.image_path)
            self.display_image()

    def display_image(self):
        self.displayed_image = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.displayed_image)
        
    def encrypt_image(self):
        if self.image_path:
            key = self.key_entry.get()
            if len(key) != 16:
                messagebox.showerror("Error", "Key must be 16 characters (128 bits) long.")
                return
            key = bytes(key, 'utf-8')
            cipher = AES.new(key, AES.MODE_ECB)
            image_data = pad(self.img.tobytes(), AES.block_size)
            encrypted_data = cipher.encrypt(image_data)

            encrypted_image_path = os.path.splitext(self.image_path)[0] + "_encrypted.png"
            with open(encrypted_image_path, "wb") as f:
                f.write(encrypted_data)

            messagebox.showinfo("Success", "Image encrypted successfully!")
        else:
            messagebox.showerror("Error", "Please upload an image first!")

    def decrypt_image(self):
        if self.image_path:
            key = self.key_entry.get()
            if len(key) != 16:
                messagebox.showerror("Error", "Key must be 16 characters (128 bits) long.")
                return
            key = bytes(key, 'utf-8')
            cipher = AES.new(key, AES.MODE_ECB)
            with open(self.image_path, "rb") as f:
                encrypted_data = f.read()
            decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
            decrypted_image = Image.frombytes("RGB", self.img.size, decrypted_data)
            
            decrypted_image.show()
        else:
            messagebox.showerror("Error", "Please upload an image first!")

    def drag_motion(self, event):
        x, y = event.x, event.y
        delta_x, delta_y = x - self.drag_data["x"], y - self.drag_data["y"]
        self.canvas.move("dragged", delta_x, delta_y)
        self.drag_data["x"], self.drag_data["y"] = x, y

    def drag_release(self, event):
        self.drag_data["x"], self.drag_data["y"] = 0, 0

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptionApp(root)
    root.mainloop()
