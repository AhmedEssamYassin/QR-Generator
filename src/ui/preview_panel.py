import customtkinter as ctk
from PIL import Image, ImageTk


class PreviewPanel:
    """Panel for displaying QR code preview"""
    
    def __init__(self, parent, mainView):
        self.mainView = mainView
        
        # Title
        title = ctk.CTkLabel(
            parent,
            text="Preview",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)
        
        # Preview canvas
        self.previewFrame = ctk.CTkFrame(
            parent,
            width=500,
            height=500
        )
        self.previewFrame.pack(expand=True, padx=20, pady=20)
        self.previewFrame.pack_propagate(False)
        
        self.previewLabel = ctk.CTkLabel(
            self.previewFrame,
            text="QR Code will appear here",
            font=ctk.CTkFont(size=16)
        )
        self.previewLabel.pack(expand=True)
        
        # Info label
        self.infoLabel = ctk.CTkLabel(
            parent,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.infoLabel.pack(pady=10)
    
    def updateImage(self, image: Image.Image) -> None:
        """Update QR code preview with new image"""
        # Resize for display
        displaySize = (450, 450)
        imgCopy = image.copy()
        imgCopy.thumbnail(displaySize, Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(imgCopy)
        self.previewLabel.configure(image=photo, text="")
        self.previewLabel.image = photo
        
        # Update info
        size = image.size
        self.infoLabel.configure(text=f"Size: {size[0]}x{size[1]} pixels")