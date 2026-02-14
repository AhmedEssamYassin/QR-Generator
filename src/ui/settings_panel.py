import tkinter as tk
from tkinter import ttk
from core.models import QRStyle
from ui.theme import FONTS, SPACING, COLORS


class SettingsPanel:
    """Panel for QR code settings and customization"""
    
    def __init__(self, parent, mainView):
        self.mainView = mainView
        
        # --- Settings Section ---
        self.settingsContent = self._createCollapsibleSection(parent, "Settings")
        
        # 1. Theme Toggle
        themeFrame = ttk.Frame(self.settingsContent)
        themeFrame.pack(fill="x", padx=SPACING['sm'], pady=SPACING['sm'])
        ttk.Label(themeFrame, text="Theme:", font=FONTS['body']).pack(side="left")
        themeBtn = ttk.Button(
            themeFrame, 
            text="Switch Mode", 
            command=lambda: self.mainView.controller.toggleTheme(),
            width=15,
            cursor="hand2"
        )
        themeBtn.pack(side="right")
        
        # 2. Error Correction
        ecFrame = ttk.Frame(self.settingsContent)
        ecFrame.pack(fill="x", padx=SPACING['sm'], pady=SPACING['sm'])
        
        ttk.Label(ecFrame, text="Error Correction:", font=FONTS['body']).pack(side="left")
        ecMenu = ttk.Combobox(
            ecFrame,
            textvariable=self.mainView.errorCorrectionVar,
            values=["LOW", "MEDIUM", "QUARTILE", "HIGH"],
            state="readonly",
            width=15,
            font=FONTS['body'],
            cursor="hand2"
        )
        ecMenu.pack(side="right")
        self._setComboboxCursor(ecMenu)

        # 3. Box Size
        sizeFrame = ttk.Frame(self.settingsContent)
        sizeFrame.pack(fill="x", padx=SPACING['sm'], pady=SPACING['sm'])
        
        ttk.Label(sizeFrame, text="Box Size:", font=FONTS['body']).pack(side="left")
        sizeSlider = ttk.Scale(
            sizeFrame,
            from_=5,
            to=20,
            variable=self.mainView.boxSizeVar,
            orient="horizontal",
            length=150,
            cursor="hand2"
        )
        sizeSlider.pack(side="right")
        
        # 4. Border
        borderFrame = ttk.Frame(self.settingsContent)
        borderFrame.pack(fill="x", padx=SPACING['sm'], pady=SPACING['sm'])
        
        ttk.Label(borderFrame, text="Border:", font=FONTS['body']).pack(side="left")
        borderSlider = ttk.Scale(
            borderFrame,
            from_=1,
            to=10,
            variable=self.mainView.borderVar,
            orient="horizontal",
            length=150,
            cursor="hand2"
        )
        borderSlider.pack(side="right")
        
        # 5. Style
        styleFrame = ttk.Frame(self.settingsContent)
        styleFrame.pack(fill="x", padx=SPACING['sm'], pady=(SPACING['sm'], SPACING['md']))
        
        ttk.Label(styleFrame, text="Style:", font=FONTS['body']).pack(side="left")
        styleMenu = ttk.Combobox(
            styleFrame,
            textvariable=self.mainView.styleVar,
            values=[s.value for s in QRStyle],
            state="readonly",
            width=15,
            font=FONTS['body'],
            cursor="hand2"
        )
        styleMenu.pack(side="right")
        self._setComboboxCursor(styleMenu)
        # --- Colors Section ---
        self.colorsContent = self._createCollapsibleSection(parent, "Colors")
        
        # Foreground Color
        fgFrame = ttk.Frame(self.colorsContent)
        fgFrame.pack(fill="x", padx=SPACING['sm'], pady=SPACING['sm'])
        
        ttk.Label(fgFrame, text="Foreground:", font=FONTS['body']).pack(side="left")

        # Create a frame to hold the color button with canvas preview
        fgButtonFrame = tk.Frame(fgFrame, relief="solid", borderwidth=1, cursor="hand2")
        fgButtonFrame.pack(side="right")
        fgButtonFrame.bind("<Button-1>", lambda e: self.mainView.controller.chooseColor("fg"))
        
        self.fgColorCanvas = tk.Canvas(fgButtonFrame, width=60, height=24, highlightthickness=0, cursor="hand2")
        self.fgColorCanvas.pack()
        self.fgColorCanvas.create_rectangle(0, 0, 60, 24, fill=self.mainView.fgColorVar.get(), outline="")
        self.fgColorCanvas.bind("<Button-1>", lambda e: self.mainView.controller.chooseColor("fg"))
        
        # Background Color
        bgFrame = ttk.Frame(self.colorsContent)
        bgFrame.pack(fill="x", padx=SPACING['sm'], pady=(SPACING['sm'], SPACING['md']))
        
        ttk.Label(bgFrame, text="Background:", font=FONTS['body']).pack(side="left")
        
        bgButtonFrame = tk.Frame(bgFrame, relief="solid", borderwidth=1, cursor="hand2")
        bgButtonFrame.pack(side="right")
        bgButtonFrame.bind("<Button-1>", lambda e: self.mainView.controller.chooseColor("bg"))
        
        self.bgColorCanvas = tk.Canvas(bgButtonFrame, width=60, height=24, highlightthickness=0, cursor="hand2")
        self.bgColorCanvas.pack()
        self.bgColorCanvas.create_rectangle(0, 0, 60, 24, fill=self.mainView.bgColorVar.get(), outline="")
        self.bgColorCanvas.bind("<Button-1>", lambda e: self.mainView.controller.chooseColor("bg"))
        
        
    def _createCollapsibleSection(self, parent, title):
        """Helper to create a collapsible frame with a header"""
        container = ttk.LabelFrame(parent, text="", padding=0)
        container.pack(fill="x", padx=SPACING['md'], pady=(0, SPACING['lg']))
        
        # State tracking - Set to False for collapsed by default
        isExpanded = [False] 
        
        # Header Button
        headerBtn = ttk.Button(
            container,
            text=f"▶ {title}",  # Default arrow for collapsed
            command=None,  # Will be set in toggle function
            style="Flat.TButton",
            cursor="hand2"
        )
        headerBtn.pack(fill="x", padx=2, pady=2, side="top")
        
        # Content frame
        contentFrame = ttk.Frame(container)
        # NOTE: We do NOT pack contentFrame here, so it starts hidden
        
        def toggle():
            if isExpanded[0]:
                contentFrame.pack_forget()
                headerBtn.configure(text=f"▶ {title}")
                isExpanded[0] = False
            else:
                contentFrame.pack(fill="x", padx=SPACING['sm'], pady=SPACING['sm'])
                headerBtn.configure(text=f"▼ {title}")
                isExpanded[0] = True
        
        headerBtn.configure(command=toggle)
        
        return contentFrame

    def updateColorButton(self, buttonType: str, color: str) -> None:
        """Update color button appearance"""
        if buttonType == "fg":
            # Clear canvas and redraw with new color
            self.fgColorCanvas.delete("all")
            self.fgColorCanvas.create_rectangle(0, 0, 60, 24, fill=color, outline="")
        else:
            # Clear canvas and redraw with new color
            self.bgColorCanvas.delete("all")
            self.bgColorCanvas.create_rectangle(0, 0, 60, 24, fill=color, outline="")


    def _setComboboxCursor(self, combobox):
        """Set hand cursor on all parts of combobox including dropdown arrow"""
        try:
            # Bind cursor to enter/leave events for the entire combobox
            combobox.bind('<Enter>', lambda e: combobox.config(cursor='hand2'))
            # Also set cursor on all child widgets (including the dropdown button)
            for child in combobox.winfo_children():
                child.configure(cursor='hand2')
        except:
            pass  # Ignore if unable to set cursor on some widgets
        