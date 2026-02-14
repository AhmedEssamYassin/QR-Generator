import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import logging
from PIL import Image, ImageTk
from typing import Dict

from core.models import QRType, QRStyle
from ui.input_panel import InputPanel
from ui.settings_panel import SettingsPanel
from ui.preview_panel import PreviewPanel
from ui.theme import FONTS, SPACING, TTK_THEME, TTK_THEME_DARK

logger = logging.getLogger(__name__)


def resourcePath(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class ScrollableFrame(ttk.Frame):
    """A scrollable frame implementation for the left panel"""
    
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollableFrame = ttk.Frame(self.canvas)
        
        self.scrollableFrame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvasFrame = self.canvas.create_window((0, 0), window=self.scrollableFrame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Bind canvas width to frame width
        self.canvas.bind('<Configure>', self._onCanvasConfigure)
        
        # Pack widgets
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel binding
        self.canvas.bind_all("<MouseWheel>", self._onMouseWheel)
        
    def _onCanvasConfigure(self, event):
        """Ensure the scrollable frame width matches canvas width"""
        self.canvas.itemconfig(self.canvasFrame, width=event.width)
        
    def _onMouseWheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class QRGeneratorView(ttkb.Window):
    """Main application window"""
    
    def __init__(self, controller, settingsService):
        # Initialize ttkbootstrap window with theme
        theme = settingsService.get("theme", "light")
        themeName = TTK_THEME if theme == "light" else TTK_THEME_DARK
        
        super().__init__(themename=themeName)
        
        self.controller = controller
        self.settingsService = settingsService
        self.currentTheme = theme
        
        # Window setup
        self.title("QR Code Generator Pro")

        # Center the window
        self._centerWindow(1000, 700)
        self.minsize(900, 600)

        # --- Icon Setup ---
        try:
            # Use resourcePath to find the icon inside the EXE bundle
            iconPath = resourcePath(os.path.join("assets", "images", "icon.ico"))
            
            if os.path.exists(iconPath):
                self.iconbitmap(iconPath)
            else:                
                logger.warning(f"Icon not found at: {iconPath}")
                
        except Exception as e:
            logger.warning(f"Could not load icon: {e}")
        # -----------------------
        
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
        
        # Left panel - Scrollable Controls
        leftPanel = ScrollableFrame(self)
        leftPanel.grid(row=0, column=0, sticky="nsew", padx=(0, 1))
        
        # Right panel - Preview
        rightPanel = ttk.Frame(self)
        rightPanel.grid(row=0, column=1, sticky="nsew")
        
        # Status bar
        self.statusBar = ttk.Label(
            self,
            text="Ready",
            anchor="w",
            relief="sunken",
            font=FONTS['small']
        )
        self.statusBar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=SPACING['md'], pady=SPACING['sm'])
        
        # Create panels - pass scrollableFrame as parent for left panel content
        self.inputPanel = InputPanel(leftPanel.scrollableFrame, self)
        self.settingsPanel = SettingsPanel(leftPanel.scrollableFrame, self)
        self.previewPanel = PreviewPanel(rightPanel, self)
        
        # Action buttons
        self._createActionButtons(leftPanel.scrollableFrame)
    
    def _createActionButtons(self, parent) -> None:
        """Create action buttons"""
        btnFrame = ttk.Frame(parent)
        btnFrame.pack(fill="x", padx=SPACING['md'], pady=SPACING['md'])
        
        self.generateBtn = ttk.Button(
            btnFrame,
            text="Generate QR",
            command=self.controller.generateQr,
            style="primary.TButton",
            width=20,
            cursor="hand2"
        )
        self.generateBtn.pack(fill="x", pady=(0, SPACING['md']), ipady=SPACING['sm'])
        
        saveFrame = ttk.Frame(btnFrame)
        saveFrame.pack(fill="x")
        
        self.saveBtn = ttk.Button(
            saveFrame,
            text="Save",
            command=self.controller.saveQr,
            width=12,
            state="disabled",
            cursor="hand2"
        )
        self.saveBtn.pack(side="left", padx=(0, SPACING['sm']))
        
        self.copyBtn = ttk.Button(
            saveFrame,
            text="Copy",
            command=self.controller.copyToClipboard,
            width=12,
            state="disabled",
            cursor="hand2"
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
        messagebox.showerror(title, message)
    
    def showInfo(self, title: str, message: str) -> None:
        """Show info dialog"""
        messagebox.showinfo(title, message)
    
    def updateColorButton(self, buttonType: str, color: str) -> None:
        """Update color button appearance"""
        self.settingsPanel.updateColorButton(buttonType, color)

    def applyTheme(self, themeName: str) -> None:
        """Apply the specified theme"""
        self.currentTheme = themeName
        # Switch ttkbootstrap theme
        newTheme = TTK_THEME if themeName == "light" else TTK_THEME_DARK
        self.style.theme_use(newTheme)