import customtkinter as ctk
from typing import Dict
from core.models import QRType


class InputPanel:
    """Panel containing input fields for QR content"""
    
    def __init__(self, parent, mainView):
        self.mainView = mainView
        self.inputFields: Dict[str, ctk.CTkBaseClass] = {}
        
        # Main container (Regular Frame, as parent is now scrollable)
        self.panelFrame = ctk.CTkFrame(parent, fg_color="transparent")
        self.panelFrame.pack(fill="x", expand=False, padx=10, pady=10)
        
        # Title
        title = ctk.CTkLabel(
            self.panelFrame,
            text="QR Code Generator",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # QR Type Selection
        typeFrame = ctk.CTkFrame(self.panelFrame)
        typeFrame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            typeFrame,
            text="QR Type",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.typeMenu = ctk.CTkOptionMenu(
            typeFrame,
            variable=self.mainView.qrTypeVar,
            values=[t.value for t in QRType],
            command=self._onTypeChange
        )
        self.typeMenu.pack(fill="x", padx=10, pady=(0, 10))
        
        # Dynamic input frame
        self.inputFrame = ctk.CTkFrame(self.panelFrame)
        self.inputFrame.pack(fill="x", pady=(0, 15))
        
        self._createInputFields(QRType.TEXT)
    
    def _createInputFields(self, qrType: QRType) -> None:
        """Create input fields based on QR type"""
        # Clear existing fields
        for widget in self.inputFrame.winfo_children():
            widget.destroy()
        self.inputFields.clear()
        
        ctk.CTkLabel(
            self.inputFrame,
            text="Content",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        if qrType == QRType.TEXT:
            textBox = ctk.CTkTextbox(self.inputFrame, height=100)
            textBox.pack(fill="x", padx=10, pady=(0, 10))
            self.inputFields['text'] = textBox
            
        elif qrType == QRType.URL:
            urlEntry = ctk.CTkEntry(self.inputFrame, placeholder_text="https://example.com")
            urlEntry.pack(fill="x", padx=10, pady=(0, 10))
            self.inputFields['url'] = urlEntry
            
        elif qrType == QRType.EMAIL:
            emailEntry = ctk.CTkEntry(self.inputFrame, placeholder_text="Email address")
            emailEntry.pack(fill="x", padx=10, pady=5)
            self.inputFields['email'] = emailEntry
            
            subjectEntry = ctk.CTkEntry(self.inputFrame, placeholder_text="Subject (optional)")
            subjectEntry.pack(fill="x", padx=10, pady=5)
            self.inputFields['subject'] = subjectEntry
            
            bodyBox = ctk.CTkTextbox(self.inputFrame, height=60)
            bodyBox.insert("1.0", "Message body (optional)")
            bodyBox.pack(fill="x", padx=10, pady=(5, 10))
            self.inputFields['body'] = bodyBox
            
        elif qrType == QRType.PHONE:
            phoneEntry = ctk.CTkEntry(self.inputFrame, placeholder_text="Phone number")
            phoneEntry.pack(fill="x", padx=10, pady=(0, 10))
            self.inputFields['phone'] = phoneEntry
            
        elif qrType == QRType.WIFI:
            ssidEntry = ctk.CTkEntry(self.inputFrame, placeholder_text="Network SSID")
            ssidEntry.pack(fill="x", padx=10, pady=5)
            self.inputFields['ssid'] = ssidEntry
            
            passwordEntry = ctk.CTkEntry(self.inputFrame, placeholder_text="Password", show="*")
            passwordEntry.pack(fill="x", padx=10, pady=5)
            self.inputFields['password'] = passwordEntry
            
            securityMenu = ctk.CTkOptionMenu(
                self.inputFrame,
                values=["WPA", "WEP", "nopass"]
            )
            securityMenu.pack(fill="x", padx=10, pady=5)
            self.inputFields['security'] = securityMenu
            
            hiddenCheck = ctk.CTkCheckBox(self.inputFrame, text="Hidden network")
            hiddenCheck.pack(anchor="w", padx=10, pady=(5, 10))
            self.inputFields['hidden'] = hiddenCheck
            
        elif qrType == QRType.VCARD:
            nameEntry = ctk.CTkEntry(self.inputFrame, placeholder_text="Full name")
            nameEntry.pack(fill="x", padx=10, pady=5)
            self.inputFields['name'] = nameEntry
            
            phoneEntry = ctk.CTkEntry(self.inputFrame, placeholder_text="Phone")
            phoneEntry.pack(fill="x", padx=10, pady=5)
            self.inputFields['phone'] = phoneEntry
            
            emailEntry = ctk.CTkEntry(self.inputFrame, placeholder_text="Email")
            emailEntry.pack(fill="x", padx=10, pady=5)
            self.inputFields['email'] = emailEntry
            
            orgEntry = ctk.CTkEntry(self.inputFrame, placeholder_text="Organization")
            orgEntry.pack(fill="x", padx=10, pady=(5, 10))
            self.inputFields['organization'] = orgEntry
    
    def _onTypeChange(self, choice: str) -> None:
        """Handle QR type change"""
        qrType = QRType(choice)
        self._createInputFields(qrType)
        
    def getData(self) -> Dict[str, str]:
        """Retrieve all input field data"""
        data = {}
        for key, widget in self.inputFields.items():
            if isinstance(widget, ctk.CTkTextbox):
                data[key] = widget.get("1.0", "end-1c")
            elif isinstance(widget, ctk.CTkEntry):
                data[key] = widget.get()
            elif isinstance(widget, ctk.CTkOptionMenu):
                data[key] = widget.get()
            elif isinstance(widget, ctk.CTkCheckBox):
                data[key] = widget.get()
        return data