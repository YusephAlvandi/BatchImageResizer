"""
Batch Image Resizer Pro - A Professional Image Processing Tool
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
        self.window.geometry("1000x750")
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
        # ===== HEADER =====
        header = ctk.CTkFrame(self.window, fg_color="transparent")
        header.pack(fill="x", pady=(30, 20), padx=40)
        
        ctk.CTkLabel(
            header, 
            text="📸 Batch Image Resizer Pro",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#1E90FF"
        ).pack()
        
        ctk.CTkLabel(
            header,
            text="Resize multiple images at once with professional quality",
            font=ctk.CTkFont(size=14),
            text_color="#AAAAAA"
        ).pack(pady=5)
        
        # ===== MAIN CONTENT =====
        main = ctk.CTkFrame(self.window, fg_color="#1a1a1a", corner_radius=16, border_width=1, border_color="#333333")
        main.pack(fill="both", expand=True, padx=40, pady=10)
        
        # ---- Folder Selection ----
        folder_section = self.create_section(main, "📁 Folder Selection")
        folder_section.pack(fill="x", padx=25, pady=(20, 10))
        
        # Input folder
        input_row = ctk.CTkFrame(folder_section, fg_color="transparent")
        input_row.pack(fill="x", pady=8)
        ctk.CTkLabel(input_row, text="Input:", font=ctk.CTkFont(size=13, weight="bold"), width=60).pack(side="left")
        ctk.CTkButton(input_row, text="Browse", width=100, height=32, corner_radius=8, 
                     command=self.select_input, font=ctk.CTkFont(size=12)).pack(side="left", padx=10)
        self.label_input = ctk.CTkLabel(input_row, text="Not selected", text_color="#888888", font=ctk.CTkFont(size=12))
        self.label_input.pack(side="left")
        
        # Output folder
        output_row = ctk.CTkFrame(folder_section, fg_color="transparent")
        output_row.pack(fill="x", pady=8)
        ctk.CTkLabel(output_row, text="Output:", font=ctk.CTkFont(size=13, weight="bold"), width=60).pack(side="left")
        ctk.CTkButton(output_row, text="Browse", width=100, height=32, corner_radius=8,
                     command=self.select_output, font=ctk.CTkFont(size=12)).pack(side="left", padx=10)
        self.label_output = ctk.CTkLabel(output_row, text="Not selected", text_color="#888888", font=ctk.CTkFont(size=12))
        self.label_output.pack(side="left")
        
        # ---- Size Settings ----
        size_section = self.create_section(main, "📐 Size Settings")
        size_section.pack(fill="x", padx=25, pady=10)
        
        size_row = ctk.CTkFrame(size_section, fg_color="transparent")
        size_row.pack(fill="x", pady=8)
        
        # Width
        w_frame = ctk.CTkFrame(size_row, fg_color="transparent")
        w_frame.pack(side="left", padx=(0, 30))
        ctk.CTkLabel(w_frame, text="Width (px):", font=ctk.CTkFont(size=13)).pack(side="left")
        ctk.CTkEntry(w_frame, textvariable=self.target_width, width=100, height=30, corner_radius=6).pack(side="left", padx=5)
        
        # Height
        h_frame = ctk.CTkFrame(size_row, fg_color="transparent")
        h_frame.pack(side="left", padx=(0, 30))
        ctk.CTkLabel(h_frame, text="Height (px):", font=ctk.CTkFont(size=13)).pack(side="left")
        ctk.CTkEntry(h_frame, textvariable=self.target_height, width=100, height=30, corner_radius=6).pack(side="left", padx=5)
        
        # Aspect ratio
        self.aspect_check = ctk.CTkCheckBox(
            size_row, text="Keep aspect ratio", variable=self.keep_aspect_ratio,
            font=ctk.CTkFont(size=13)
        )
        self.aspect_check.pack(side="left", padx=20)
        
        # ---- Output Settings ----
        output_section = self.create_section(main, "⚙️ Output Settings")
        output_section.pack(fill="x", padx=25, pady=10)
        
        settings_row = ctk.CTkFrame(output_section, fg_color="transparent")
        settings_row.pack(fill="x", pady=8)
        
        # Format selector
        fmt_frame = ctk.CTkFrame(settings_row, fg_color="transparent")
        fmt_frame.pack(side="left", padx=(0, 30))
        ctk.CTkLabel(fmt_frame, text="Format:", font=ctk.CTkFont(size=13)).pack(side="left")
        ctk.CTkComboBox(
            fmt_frame, values=["JPEG", "PNG", "WebP", "BMP"],
            variable=self.output_format, width=120, height=30,
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=5)
        
        # Quality slider
        qual_frame = ctk.CTkFrame(settings_row, fg_color="transparent")
        qual_frame.pack(side="left")
        ctk.CTkLabel(qual_frame, text="Quality:", font=ctk.CTkFont(size=13)).pack(side="left")
        ctk.CTkSlider(qual_frame, from_=10, to=100, variable=self.quality, width=200, command=self.update_quality_label).pack(side="left", padx=5)
        self.qual_label = ctk.CTkLabel(qual_frame, text="90%", font=ctk.CTkFont(size=13, weight="bold"))
        self.qual_label.pack(side="left", padx=5)
        
        # ---- Process Button ----
        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(fill="x", padx=25, pady=(20, 25))
        
        self.btn_process = ctk.CTkButton(
            btn_frame, text="🚀 Start Resizing", command=self.process_images,
            height=48, font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#1E90FF", hover_color="#3578E6", corner_radius=12
        )
        self.btn_process.pack(fill="x")
        
        # ===== STATUS BAR =====
        status_frame = ctk.CTkFrame(self.window, fg_color="#1a1a1a", corner_radius=12, height=45)
        status_frame.pack(fill="x", padx=40, pady=(0, 20))
        status_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="● Ready to resize images",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#4CAF50"
        )
        self.status_label.pack(pady=10)
    
    def create_section(self, parent, title):
        """Create a titled section frame"""
        section = ctk.CTkFrame(parent, fg_color="#252525", corner_radius=10)
        ctk.CTkLabel(
            section, text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#1E90FF"
        ).pack(anchor="w", padx=15, pady=(12, 5))
        return section
    
    def select_input(self):
        """Select input folder"""
        self.input_folder = filedialog.askdirectory(title="Select Input Folder")
        if self.input_folder:
            self.label_input.configure(text=f"✓ {os.path.basename(self.input_folder)}", text_color="#4CAF50")
    
    def select_output(self):
        """Select output folder"""
        self.output_folder = filedialog.askdirectory(title="Select Output Folder")
        if self.output_folder:
            self.label_output.configure(text=f"✓ {os.path.basename(self.output_folder)}", text_color="#4CAF50")
    
    def update_quality_label(self, value):
        """Update quality percentage label"""
        self.qual_label.configure(text=f"{int(float(value))}%")
    
    def process_images(self):
        """Process all images in the input folder"""
        # 1. Validation
        if not self.input_folder:
            messagebox.showerror("Error", "Please select input folder!")
            return
        if not self.output_folder:
            messagebox.showerror("Error", "Please select output folder!")
            return
        
        # 2. Get settings
        target_size = (self.target_width.get(), self.target_height.get())
        output_fmt = self.output_format.get()
        quality_val = self.quality.get()
        
        # 3. Supported image formats
        supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')
        
        # 4. Process images
        processed_count = 0
        skipped_count = 0
        
        self.btn_process.configure(state="disabled", text="⏳ Processing...")
        self.window.update()
        
        for filename in os.listdir(self.input_folder):
            if filename.lower().endswith(supported_formats):
                input_path = os.path.join(self.input_folder, filename)
                
                try:
                    # Open image
                    img = Image.open(input_path)
                    original_size = img.size
                    
                    # Resize with or without keeping aspect ratio
                    if self.keep_aspect_ratio.get():
                        img.thumbnail(target_size, Image.Resampling.LANCZOS)
                    else:
                        img = img.resize(target_size, Image.Resampling.LANCZOS)
                    
                    # Create output filename
                    name_without_ext = os.path.splitext(filename)[0]
                    output_filename = f"{name_without_ext}_{img.size[0]}x{img.size[1]}.{output_fmt.lower()}"
                    output_path = os.path.join(self.output_folder, output_filename)
                    
                    # Convert RGBA to RGB for JPEG format
                    if output_fmt.upper() in ['JPEG', 'JPG'] and img.mode == 'RGBA':
                        img = img.convert('RGB')
                    
                    # Save image
                    img.save(output_path, format=output_fmt.upper(), quality=quality_val if output_fmt.upper() == 'JPEG' else None)
                    
                    processed_count += 1
                    self.status_label.configure(
                        text=f"🔄 Processing: {filename} ({original_size[0]}x{original_size[1]} → {img.size[0]}x{img.size[1]})",
                        text_color="#FFAA33"
                    )
                    self.window.update()
                    
                except Exception as e:
                    skipped_count += 1
                    self.status_label.configure(
                        text=f"⚠️ Skipped: {filename} - {str(e)}",
                        text_color="#FF5555"
                    )
                    self.window.update()
        
        # 5. Show completion message
        self.btn_process.configure(state="normal", text="🚀 Start Resizing")
        
        if processed_count > 0:
            self.status_label.configure(
                text=f"✅ Done! {processed_count} images resized, {skipped_count} skipped",
                text_color="#4CAF50"
            )
            messagebox.showinfo(
                "Success",
                f"Successfully resized {processed_count} images!\n\n"
                f"Format: {output_fmt}\n"
                f"Size: {target_size[0]}×{target_size[1]} px\n"
                f"Saved to: {os.path.basename(self.output_folder)}"
            )
        else:
            self.status_label.configure(
                text="⚠️ No images found in input folder",
                text_color="#FFAA33"
            )
    
    def run(self):
        """Run the application"""
        self.window.mainloop()

if __name__ == "__main__":
    app = ImageResizerApp()
    app.run()