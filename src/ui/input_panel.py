import tkinter as tk
from tkinter import ttk
from typing import Dict
from core.models import QRType
from ui.theme import FONTS, SPACING


class InputPanel:
    """Panel containing input fields for QR content"""
    
    def __init__(self, parent, mainView):
        self.mainView = mainView
        self.inputFields: Dict[str, tk.Widget] = {}
        
        # Main container (Regular Frame, as parent is now scrollable)
        self.panelFrame = ttk.Frame(parent)
        self.panelFrame.pack(fill="x", expand=False, padx=SPACING['md'], pady=SPACING['md'])
        
        # Title
        title = ttk.Label(
            self.panelFrame,
            text="QR Code Generator",
            font=FONTS['title']
        )
        title.pack(pady=(0, SPACING['xl']))
        
        # QR Type Selection
        typeFrame = ttk.LabelFrame(self.panelFrame, text="QR Type", padding=SPACING['md'])
        typeFrame.pack(fill="x", pady=(0, SPACING['lg']))
        
        self.typeMenu = ttk.Combobox(
            typeFrame,
            textvariable=self.mainView.qrTypeVar,
            values=[t.value for t in QRType],
            state="readonly",
            font=FONTS['body'],
            cursor="hand2"
        )
        self.typeMenu.pack(fill="x")
        self.typeMenu.bind('<<ComboboxSelected>>', self._onTypeChange)
        self._setComboboxCursor(self.typeMenu)
        # Dynamic input frame
        self.inputFrame = ttk.LabelFrame(self.panelFrame, text="Content", padding=SPACING['md'])
        self.inputFrame.pack(fill="x", pady=(0, SPACING['lg']))
        
        self._createInputFields(QRType.TEXT)
    
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
        
    def _createInputFields(self, qrType: QRType) -> None:
        """Create input fields based on QR type"""
        # Clear existing fields
        for widget in self.inputFrame.winfo_children():
            widget.destroy()
        self.inputFields.clear()
        
        if qrType == QRType.TEXT:
            textBox = tk.Text(
                self.inputFrame, 
                height=5, 
                font=FONTS['body'],
                relief="solid",
                borderwidth=1
            )
            textBox.pack(fill="x", pady=SPACING['sm'])
            self.inputFields['text'] = textBox
            
        elif qrType == QRType.URL:
            urlEntry = ttk.Entry(self.inputFrame, font=FONTS['body'])
            urlEntry.insert(0, "https://example.com")
            urlEntry.bind("<FocusIn>", lambda e: urlEntry.delete(0, 'end') if urlEntry.get() == "https://example.com" else None)
            urlEntry.pack(fill="x", pady=SPACING['sm'])
            self.inputFields['url'] = urlEntry
            
        elif qrType == QRType.EMAIL:
            ttk.Label(self.inputFrame, text="Email Address:", font=FONTS['body']).pack(anchor="w", pady=(SPACING['sm'], SPACING['xs']))
            emailEntry = ttk.Entry(self.inputFrame, font=FONTS['body'])
            emailEntry.pack(fill="x", pady=(0, SPACING['sm']))
            self.inputFields['email'] = emailEntry
            
            ttk.Label(self.inputFrame, text="Subject (optional):", font=FONTS['body']).pack(anchor="w", pady=(SPACING['sm'], SPACING['xs']))
            subjectEntry = ttk.Entry(self.inputFrame, font=FONTS['body'])
            subjectEntry.pack(fill="x", pady=(0, SPACING['sm']))
            self.inputFields['subject'] = subjectEntry
            
            ttk.Label(self.inputFrame, text="Message Body (optional):", font=FONTS['body']).pack(anchor="w", pady=(SPACING['sm'], SPACING['xs']))
            bodyBox = tk.Text(
                self.inputFrame, 
                height=3, 
                font=FONTS['body'],
                relief="solid",
                borderwidth=1
            )
            bodyBox.pack(fill="x", pady=(0, SPACING['sm']))
            self.inputFields['body'] = bodyBox
            
        elif qrType == QRType.PHONE:
            ttk.Label(self.inputFrame, text="Phone Number:", font=FONTS['body']).pack(anchor="w", pady=(SPACING['sm'], SPACING['xs']))
            phoneEntry = ttk.Entry(self.inputFrame, font=FONTS['body'])
            phoneEntry.pack(fill="x", pady=(0, SPACING['sm']))
            self.inputFields['phone'] = phoneEntry
            
        elif qrType == QRType.WIFI:
            ttk.Label(self.inputFrame, text="Network SSID:", font=FONTS['body']).pack(anchor="w", pady=(SPACING['sm'], SPACING['xs']))
            ssidEntry = ttk.Entry(self.inputFrame, font=FONTS['body'])
            ssidEntry.pack(fill="x", pady=(0, SPACING['sm']))
            self.inputFields['ssid'] = ssidEntry
            
            ttk.Label(self.inputFrame, text="Password:", font=FONTS['body']).pack(anchor="w", pady=(SPACING['sm'], SPACING['xs']))
            passwordEntry = ttk.Entry(self.inputFrame, font=FONTS['body'], show="*")
            passwordEntry.pack(fill="x", pady=(0, SPACING['sm']))
            self.inputFields['password'] = passwordEntry
            
            ttk.Label(self.inputFrame, text="Security:", font=FONTS['body']).pack(anchor="w", pady=(SPACING['sm'], SPACING['xs']))
            securityMenu = ttk.Combobox(
                self.inputFrame,
                values=["WPA", "WEP", "nopass"],
                state="readonly",
                font=FONTS['body']
            )
            securityMenu.current(0)
            securityMenu.pack(fill="x", pady=(0, SPACING['sm']))
            self.inputFields['security'] = securityMenu
            
            hiddenCheck = ttk.Checkbutton(self.inputFrame, text="Hidden network", cursor="hand2")
            hiddenCheck.pack(anchor="w", pady=(SPACING['sm'], 0))
            self.inputFields['hidden'] = hiddenCheck
            
        elif qrType == QRType.VCARD:
            ttk.Label(self.inputFrame, text="Full Name:", font=FONTS['body']).pack(anchor="w", pady=(SPACING['sm'], SPACING['xs']))
            nameEntry = ttk.Entry(self.inputFrame, font=FONTS['body'], cursor="hand2")
            nameEntry.pack(fill="x", pady=(0, SPACING['sm']))
            self.inputFields['name'] = nameEntry
            
            ttk.Label(self.inputFrame, text="Phone:", font=FONTS['body']).pack(anchor="w", pady=(SPACING['sm'], SPACING['xs']))
            phoneEntry = ttk.Entry(self.inputFrame, font=FONTS['body'], cursor="hand2")
            phoneEntry.pack(fill="x", pady=(0, SPACING['sm']))
            self.inputFields['phone'] = phoneEntry
            
            ttk.Label(self.inputFrame, text="Email:", font=FONTS['body']).pack(anchor="w", pady=(SPACING['sm'], SPACING['xs']))
            emailEntry = ttk.Entry(self.inputFrame, font=FONTS['body'], cursor="hand2")
            emailEntry.pack(fill="x", pady=(0, SPACING['sm']))
            self.inputFields['email'] = emailEntry
            
            ttk.Label(self.inputFrame, text="Organization:", font=FONTS['body']).pack(anchor="w", pady=(SPACING['sm'], SPACING['xs']))
            orgEntry = ttk.Entry(self.inputFrame, font=FONTS['body'], cursor="hand2")
            orgEntry.pack(fill="x", pady=(0, SPACING['sm']))
            self.inputFields['organization'] = orgEntry
    
    def _onTypeChange(self, event=None) -> None:
        """Handle QR type change"""
        choice = self.mainView.qrTypeVar.get()
        qrType = QRType(choice)
        self._createInputFields(qrType)
        
    def getData(self) -> Dict[str, str]:
        """Retrieve all input field data"""
        data = {}
        for key, widget in self.inputFields.items():
            if isinstance(widget, tk.Text):
                data[key] = widget.get("1.0", "end-1c")
            elif isinstance(widget, ttk.Entry):
                data[key] = widget.get()
            elif isinstance(widget, ttk.Combobox):
                data[key] = widget.get()
            elif isinstance(widget, ttk.Checkbutton):
                # For checkbuttons, we need to track their state via a variable
                # Since we're maintaining compatibility, we check the widget state
                try:
                    data[key] = widget.instate(['selected'])
                except:
                    data[key] = False
        return data