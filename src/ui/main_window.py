import os
import tkinter as tk
import customtkinter as ctk
import logging
from PIL import Image, ImageTk
from typing import Dict

from core.models import QRType, QRStyle
from ui.input_panel import InputPanel
from ui.settings_panel import SettingsPanel
from ui.preview_panel import PreviewPanel

logger = logging.getLogger(__name__)


class QRGeneratorView(ctk.CTk):
    """Main application window"""
    
    def __init__(self, controller, settingsService):
        super().__init__()
        
        self.controller = controller
        self.settingsService = settingsService
        
        # Window setup
        self.title("QR Code Generator Pro")

        # Center the window
        self._centerWindow(1000, 700)
        self.minsize(900, 600)

        # --- Icon Setup ---
        try:
            iconPath = os.path.join("assets", "images", "icon.ico")
            
            if os.path.exists(iconPath):
                self.iconbitmap(iconPath)
            else:                
                logger.warning(f"Icon not found at: {iconPath}")
                
        except Exception as e:
            logger.warning(f"Could not load icon: {e}")
        # -----------------------
        
        # Apply theme
        theme = self.settingsService.get("theme", "light")
        self.applyTheme(theme)
        ctk.set_default_color_theme("blue")
        
        # Variables
        self.qrTypeVar = tk.StringVar(value=QRType.TEXT.value)
        self.errorCorrectionVar = tk.StringVar(value="HIGH")
        self.boxSizeVar = tk.IntVar(value=self.settingsService.get("default_box_size", 10))
        self.borderVar = tk.IntVar(value=self.settingsService.get("default_border", 4))
        self.fgColorVar = tk.StringVar(value="#000000")
        self.bgColorVar = tk.StringVar(value="#FFFFFF")
        self.styleVar = tk.StringVar(value=QRStyle.SQUARE.value)
        
        # Build UI
        self._createLayout()
        self._bindShortcuts()
        
        logger.info("Main window initialized")
    
    def _centerWindow(self, width: int, height: int) -> None:
        """Center the window on the screen"""
        # Get screen dimensions
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()
        
        # Calculate x and y coordinates
        x = (screenWidth - width) // 2
        y = (screenHeight - height) // 2
        
        # Set geometry
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _createLayout(self) -> None:
        """Create main layout"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        
        # Left panel - Controls
        leftPanel = ctk.CTkFrame(self, corner_radius=0)
        leftPanel.grid(row=0, column=0, sticky="nsew", padx=(0, 1))
        
        # Right panel - Preview
        rightPanel = ctk.CTkFrame(self, corner_radius=0)
        rightPanel.grid(row=0, column=1, sticky="nsew")
        
        # Status bar
        self.statusBar = ctk.CTkLabel(
            self,
            text="Ready",
            anchor="w",
            height=30
        )
        self.statusBar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        # Create panels
        self.inputPanel = InputPanel(leftPanel, self)
        self.settingsPanel = SettingsPanel(leftPanel, self)
        self.previewPanel = PreviewPanel(rightPanel, self)
        
        # Action buttons
        self._createActionButtons(leftPanel)
    
    def _createActionButtons(self, parent) -> None:
        """Create action buttons"""
        btnFrame = ctk.CTkFrame(parent, fg_color="transparent")
        btnFrame.pack(fill="x", padx=10, pady=10)
        
        self.generateBtn = ctk.CTkButton(
            btnFrame,
            text="Generate QR",
            command=self.controller.generateQr,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.generateBtn.pack(fill="x", pady=(0, 10))
        
        saveFrame = ctk.CTkFrame(btnFrame, fg_color="transparent")
        saveFrame.pack(fill="x")
        
        self.saveBtn = ctk.CTkButton(
            saveFrame,
            text="Save",
            command=self.controller.saveQr,
            width=100,
            state="disabled"
        )
        self.saveBtn.pack(side="left", padx=(0, 5))
        
        self.copyBtn = ctk.CTkButton(
            saveFrame,
            text="Copy",
            command=self.controller.copyToClipboard,
            width=100,
            state="disabled"
        )
        self.copyBtn.pack(side="left")
    
    def _bindShortcuts(self) -> None:
        """Bind keyboard shortcuts"""
        self.bind("<Control-g>", lambda e: self.controller.generateQr())
        self.bind("<Control-s>", lambda e: self.controller.saveQr())
        self.bind("<Control-c>", lambda e: self.controller.copyToClipboard())
        self.bind("<F1>", lambda e: self.controller.showHelp())
    
    def getInputData(self) -> Dict[str, str]:
        """Retrieve all input field data"""
        return self.inputPanel.getData()
    
    def updatePreview(self, image: Image.Image) -> None:
        """Update QR code preview"""
        self.previewPanel.updateImage(image)
        self.saveBtn.configure(state="normal")
        self.copyBtn.configure(state="normal")
    
    def updateStatus(self, message: str) -> None:
        """Update status bar"""
        self.statusBar.configure(text=message)
    
    def showError(self, title: str, message: str) -> None:
        """Show error dialog"""
        from tkinter import messagebox
        messagebox.showerror(title, message)
    
    def showInfo(self, title: str, message: str) -> None:
        """Show info dialog"""
        from tkinter import messagebox
        messagebox.showinfo(title, message)
    
    def updateColorButton(self, buttonType: str, color: str) -> None:
        """Update color button appearance"""
        self.settingsPanel.updateColorButton(buttonType, color)

    def applyTheme(self, themeName: str) -> None:
        """Apply the specified theme"""
        ctk.set_appearance_mode(themeName)