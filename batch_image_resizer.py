"""
Batch Image Resizer - A Professional Image Processing Tool
Author: Yuseph Alvandi
GitHub: https://github.com/YusephAlvandi
Version: 1.0.0
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os
from datetime import datetime

# ============ GLOBAL SETTINGS ============
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
# =========================================

class ImageResizerApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Batch Image Resizer Pro")
        self.window.geometry("1000x700")
        self.window.configure(fg_color="#0a0a0a")
        
        self.input_folder = ""
        self.output_folder = ""
        
        # Default settings
        self.target_width = ctk.IntVar(value=800)
        self.target_height = ctk.IntVar(value=600)
        self.keep_aspect_ratio = ctk.BooleanVar(value=True)
        self.output_format = ctk.StringVar(value="JPEG")
        self.quality = ctk.IntVar(value=90)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title = ctk.CTkLabel(
            self.window, 
            text="📸 Batch Image Resizer Pro",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#1E90FF"
        )
        title.pack(pady=30)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.window,
            text="● Ready to resize images",
            font=ctk.CTkFont(size=14),
            text_color="#4CAF50"
        )
        self.status_label.pack(pady=10)
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ImageResizerApp()
    app.run()