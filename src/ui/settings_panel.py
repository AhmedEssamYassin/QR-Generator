import customtkinter as ctk
from core.models import QRStyle


class SettingsPanel:
    """Panel for QR code settings and customization"""
    
    def __init__(self, parent, mainView):
        self.mainView = mainView
        
        # --- Settings Section ---
        self.settingsContent = self._createCollapsibleSection(parent, "Settings")
        
        # 1. Theme Toggle
        themeFrame = ctk.CTkFrame(self.settingsContent, fg_color="transparent")
        themeFrame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(themeFrame, text="Theme:").pack(side="left")
        ctk.CTkButton(
            themeFrame, 
            text="Switch Mode", 
            command=lambda: self.mainView.controller.toggleTheme(),
            width=100,
            height=24
        ).pack(side="right")
        
        # 2. Error Correction
        ecFrame = ctk.CTkFrame(self.settingsContent, fg_color="transparent")
        ecFrame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(ecFrame, text="Error Correction:").pack(side="left")
        ctk.CTkOptionMenu(
            ecFrame,
            variable=self.mainView.errorCorrectionVar,
            values=["LOW", "MEDIUM", "QUARTILE", "HIGH"],
            width=120
        ).pack(side="right")
        
        # 3. Box Size
        sizeFrame = ctk.CTkFrame(self.settingsContent, fg_color="transparent")
        sizeFrame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(sizeFrame, text="Box Size:").pack(side="left")
        ctk.CTkSlider(
            sizeFrame,
            from_=5,
            to=20,
            number_of_steps=15,
            variable=self.mainView.boxSizeVar,
            width=150
        ).pack(side="right")
        
        # 4. Border
        borderFrame = ctk.CTkFrame(self.settingsContent, fg_color="transparent")
        borderFrame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(borderFrame, text="Border:").pack(side="left")
        ctk.CTkSlider(
            borderFrame,
            from_=1,
            to=10,
            number_of_steps=9,
            variable=self.mainView.borderVar,
            width=150
        ).pack(side="right")
        
        # 5. Style
        styleFrame = ctk.CTkFrame(self.settingsContent, fg_color="transparent")
        styleFrame.pack(fill="x", padx=5, pady=(5, 10))
        
        ctk.CTkLabel(styleFrame, text="Style:").pack(side="left")
        ctk.CTkOptionMenu(
            styleFrame,
            variable=self.mainView.styleVar,
            values=[s.value for s in QRStyle],
            width=150
        ).pack(side="right")
        
        # --- Colors Section ---
        self.colorsContent = self._createCollapsibleSection(parent, "Colors")
        
        # Foreground Color
        fgFrame = ctk.CTkFrame(self.colorsContent, fg_color="transparent")
        fgFrame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(fgFrame, text="Foreground:").pack(side="left")
        self.fgColorButton = ctk.CTkButton(
            fgFrame,
            text="",
            width=60,
            height=30,
            fg_color=self.mainView.fgColorVar.get(),
            command=lambda: self.mainView.controller.chooseColor("fg")
        )
        self.fgColorButton.pack(side="right")
        
        # Background Color
        bgFrame = ctk.CTkFrame(self.colorsContent, fg_color="transparent")
        bgFrame.pack(fill="x", padx=5, pady=(5, 10))
        
        ctk.CTkLabel(bgFrame, text="Background:").pack(side="left")
        self.bgColorButton = ctk.CTkButton(
            bgFrame,
            text="",
            width=60,
            height=30,
            fg_color=self.mainView.bgColorVar.get(),
            command=lambda: self.mainView.controller.chooseColor("bg")
        )
        self.bgColorButton.pack(side="right")
        
    def _createCollapsibleSection(self, parent, title):
        """Helper to create a collapsible frame with a header"""
        container = ctk.CTkFrame(parent)
        container.pack(fill="x", padx=10, pady=(0, 15))
        
        # State tracking - Set to False for collapsed by default
        isExpanded = [False] 
        
        # Header Button - Create AND Pack FIRST to ensure it stays at top
        headerBtn = ctk.CTkButton(
            container,
            text=f"{title} ▶",  # Default arrow for collapsed
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=30,
            cursor="hand2"  # Change cursor on hover
        )
        headerBtn.pack(fill="x", padx=2, pady=2, side="top")
        
        # Content frame - Create second
        contentFrame = ctk.CTkFrame(container, fg_color="transparent")
        # NOTE: We do NOT pack contentFrame here, so it starts hidden
        
        def toggle():
            if isExpanded[0]:
                contentFrame.pack_forget()
                headerBtn.configure(text=f"{title} ▶")
                isExpanded[0] = False
            else:
                contentFrame.pack(fill="x", padx=5, pady=5)
                headerBtn.configure(text=f"{title} ▼")
                isExpanded[0] = True
        
        headerBtn.configure(command=toggle)
        
        return contentFrame

    def updateColorButton(self, buttonType: str, color: str) -> None:
        """Update color button appearance"""
        if buttonType == "fg":
            self.fgColorButton.configure(fg_color=color)
        else:
            self.bgColorButton.configure(fg_color=color)