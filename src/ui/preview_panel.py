import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ui.theme import FONTS, SPACING


class PreviewPanel:
    """Panel for displaying QR code preview"""
    
    def __init__(self, parent, mainView):
        self.mainView = mainView
        
        # Title
        title = ttk.Label(
            parent,
            text="Preview",
            font=FONTS['heading']
        )
        title.pack(pady=SPACING['xl'])
        
        # Preview canvas - using Frame as container
        self.previewFrame = ttk.Frame(
            parent,
            width=500,
            height=500,
            relief="solid",
            borderwidth=1
        )
        self.previewFrame.pack(expand=True, padx=SPACING['xl'], pady=SPACING['xl'])
        self.previewFrame.pack_propagate(False)
        
        self.previewLabel = ttk.Label(
            self.previewFrame,
            text="QR Code will appear here",
            font=FONTS['body'],
            anchor="center"
        )
        self.previewLabel.pack(expand=True)
        
        # Info label
        self.infoLabel = ttk.Label(
            parent,
            text="",
            font=FONTS['small']
        )
        self.infoLabel.pack(pady=SPACING['md'])
    
    def updateImage(self, image: Image.Image) -> None:
        """Update QR code preview with new image"""
        # Resize for display
        displaySize = (450, 450)
        imgCopy = image.copy()
        imgCopy.thumbnail(displaySize, Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(imgCopy)
        self.previewLabel.configure(image=photo, text="")
        self.previewLabel.image = photo  # Keep reference
        
        # Update info
        size = image.size
        self.infoLabel.configure(text=f"Size: {size[0]}x{size[1]} pixels")
