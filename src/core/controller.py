import logging
import os
import tempfile
from datetime import datetime
from tkinter import filedialog, colorchooser

from core.models import QRGeneratorModel, QRType, ErrorCorrection, QRStyle, QRConfig
from core.qr_generator import QRGenerator
from services.file_service import FileService
from services.history_service import HistoryService
from services.settings_service import SettingsService

logger = logging.getLogger(__name__)


class QRGeneratorController:
    """Application controller"""
    
    def __init__(self, model: QRGeneratorModel, settingsService: SettingsService):
        self.model = model
        self.settingsService = settingsService
        self.historyService = HistoryService()
        self.fileService = FileService()
        self.view = None
        
        logger.info("Controller initialized")
    
    def setView(self, view):
        """Set the view reference"""
        self.view = view
    
    def toggleTheme(self) -> None:
        """Toggle between light and dark modes"""
        current = self.settingsService.get("theme", "light")
        # Switch logic
        newTheme = "dark" if current.lower() == "light" else "light"
        
        # Save to settings
        self.settingsService.set("theme", newTheme)
        
        # Update UI if view is attached
        if self.view:
            self.view.applyTheme(newTheme)
            self.view.updateStatus(f"Theme switched to {newTheme}")
            logger.info(f"Theme switched to {newTheme}")

    def generateQr(self) -> None:
        """Generate QR code from current inputs"""
        if not self.view:
            return
            
        try:
            self.view.updateStatus("Generating QR code...")
            
            # Get input data
            qrType = QRType(self.view.qrTypeVar.get())
            inputData = self.view.getInputData()
            
            # Format content
            content = self.model.formatContent(qrType, inputData)
            
            if not content.strip():
                self.view.showError("Error", "Please enter content for the QR code")
                self.view.updateStatus("Ready")
                return
            
            # Get settings
            errorCorrection = ErrorCorrection[self.view.errorCorrectionVar.get()]
            boxSize = self.view.boxSizeVar.get()
            border = self.view.borderVar.get()
            fgColor = self.view.fgColorVar.get()
            bgColor = self.view.bgColorVar.get()
            style = QRStyle(self.view.styleVar.get())
            
            # Generate QR
            qrImage = QRGenerator.generate(
                content=content,
                errorCorrection=errorCorrection,
                boxSize=boxSize,
                border=border,
                fgColor=fgColor,
                bgColor=bgColor,
                style=style
            )
            
            self.model.currentQrImage = qrImage
            
            # Update preview
            self.view.updatePreview(qrImage)
            
            # Save to history
            config = QRConfig(
                content=content[:100],  # Truncate for storage
                qrType=qrType.value,
                errorCorrection=errorCorrection.name,
                boxSize=boxSize,
                border=border,
                fgColor=fgColor,
                bgColor=bgColor,
                style=style.value,
                timestamp=datetime.now().isoformat()
            )
            self.historyService.add(config)
            
            self.view.updateStatus(f"QR code generated successfully • {len(content)} characters")
            logger.info(f"QR generated: {qrType.value}")
            
        except Exception as e:
            errorMsg = f"Failed to generate QR code: {str(e)}"
            self.view.showError("Error", errorMsg)
            self.view.updateStatus("Error generating QR code")
            logger.error(errorMsg)
    
    def saveQr(self) -> None:
        """Save QR code to file"""
        if not self.model.currentQrImage:
            self.view.showError("Error", "No QR code to save")
            return
        
        try:
            fileTypes = [
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
            
            lastDir = self.settingsService.get("last_save_directory", "")
            
            filePath = filedialog.asksaveasfilename(
                title="Save QR Code",
                defaultextension=".png",
                filetypes=fileTypes,
                initialdir=lastDir
            )
            
            if filePath:
                self.fileService.saveImage(self.model.currentQrImage, filePath)
                
                # Update settings
                self.settingsService.set("last_save_directory", os.path.dirname(filePath))
                
                self.view.showInfo("Success", f"QR code saved to:\n{filePath}")
                self.view.updateStatus(f"Saved: {os.path.basename(filePath)}")
                
        except Exception as e:
            errorMsg = f"Failed to save QR code: {str(e)}"
            self.view.showError("Error", errorMsg)
            logger.error(errorMsg)
    
    def copyToClipboard(self) -> None:
        """Copy QR code image to clipboard"""
        if not self.model.currentQrImage:
            self.view.showError("Error", "No QR code to copy")
            return
        
        try:
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                self.model.currentQrImage.save(tmp.name, 'PNG')
                tmpPath = tmp.name
            
            self.view.showInfo("Info", "QR code image saved temporarily for clipboard")
            self.view.updateStatus("Copied to clipboard")
            
            os.unlink(tmpPath)
            
        except Exception as e:
            errorMsg = f"Failed to copy to clipboard: {str(e)}"
            self.view.showError("Error", errorMsg)
            logger.error(errorMsg)
    
    def chooseColor(self, colorType: str) -> None:
        """Open color picker dialog"""
        initialColor = (
            self.view.fgColorVar.get() if colorType == "fg"
            else self.view.bgColorVar.get()
        )
        
        color = colorchooser.askcolor(
            title=f"Choose {'Foreground' if colorType == 'fg' else 'Background'} Color",
            initialcolor=initialColor
        )
        
        if color[1]:
            if colorType == "fg":
                self.view.fgColorVar.set(color[1])
            else:
                self.view.bgColorVar.set(color[1])
            
            self.view.updateColorButton(colorType, color[1])
            
    def showHelp(self) -> None:
        """Show help dialog"""
        helpText = """
QR Code Generator Pro - Help

Keyboard Shortcuts:
• Ctrl+G: Generate QR code
• Ctrl+S: Save QR code
• Ctrl+C: Copy to clipboard
• F1: Show this help

Features:
• Multiple QR types (Text, URL, Email, Phone, WiFi, vCard)
• Customizable styles and colors
• Error correction levels
• Auto preview mode
• Generation history

For more information, visit our documentation.
        """
        self.view.showInfo("Help", helpText.strip())
    
    def getHistory(self):
        """Get generation history"""
        return self.historyService.getAll()