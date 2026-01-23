from dataclasses import dataclass, asdict
from enum import Enum
import qrcode
from typing import Dict, Any


class QRType(Enum):
    """QR code content types"""
    TEXT = "Text"
    URL = "URL"
    EMAIL = "Email"
    PHONE = "Phone"
    WIFI = "WiFi"
    VCARD = "vCard"


class ErrorCorrection(Enum):
    """QR error correction levels"""
    LOW = (qrcode.constants.ERROR_CORRECT_L, "7% recovery")
    MEDIUM = (qrcode.constants.ERROR_CORRECT_M, "15% recovery")
    QUARTILE = (qrcode.constants.ERROR_CORRECT_Q, "25% recovery")
    HIGH = (qrcode.constants.ERROR_CORRECT_H, "30% recovery")


class QRStyle(Enum):
    """QR module drawing styles"""
    SQUARE = "Square"
    ROUNDED = "Rounded"
    CIRCLE = "Circle"
    GAPPED = "Gapped Square"


@dataclass
class QRConfig:
    """QR code configuration"""
    content: str
    qrType: str
    errorCorrection: str
    boxSize: int
    border: int
    fgColor: str
    bgColor: str
    style: str
    timestamp: str
    
    def toDict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class QRGeneratorModel:
    """Core QR generation logic and data management"""
    
    def __init__(self):
        self.currentQrImage = None
        
    def formatContent(self, qrType: QRType, data: Dict[str, str]) -> str:
        """Format content based on QR type"""
        if qrType == QRType.TEXT:
            return data.get('text', '')
        
        elif qrType == QRType.URL:
            url = data.get('url', '')
            if url and not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            return url
        
        elif qrType == QRType.EMAIL:
            email = data.get('email', '')
            subject = data.get('subject', '')
            body = data.get('body', '')
            return f"mailto:{email}?subject={subject}&body={body}"
        
        elif qrType == QRType.PHONE:
            return f"tel:{data.get('phone', '')}"
        
        elif qrType == QRType.WIFI:
            ssid = data.get('ssid', '')
            password = data.get('password', '')
            security = data.get('security', 'WPA')
            hidden = 'true' if data.get('hidden', False) else 'false'
            return f"WIFI:T:{security};S:{ssid};P:{password};H:{hidden};;"
        
        elif qrType == QRType.VCARD:
            return (
                f"BEGIN:VCARD\n"
                f"VERSION:3.0\n"
                f"FN:{data.get('name', '')}\n"
                f"TEL:{data.get('phone', '')}\n"
                f"EMAIL:{data.get('email', '')}\n"
                f"ORG:{data.get('organization', '')}\n"
                f"END:VCARD"
            )
        
        return data.get('text', '')